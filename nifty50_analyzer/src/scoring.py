"""
Scoring Module for NIFTY 50 Analyzer
Scores companies based on financial ratios vs sector benchmarks
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import yaml
import logging
from scipy import stats

logger = logging.getLogger(__name__)


class RatioScorer:
    """Score financial ratios against sector benchmarks"""

    def __init__(self, benchmarks_file: str):
        """
        Initialize scorer with sector benchmarks

        Args:
            benchmarks_file: Path to sector_benchmarks.yml
        """
        self.benchmarks = self._load_benchmarks(benchmarks_file)

    def _load_benchmarks(self, file_path: str) -> Dict:
        """Load sector benchmarks from YAML file"""
        logger.info(f"Loading sector benchmarks from {file_path}")

        try:
            with open(file_path, 'r') as f:
                benchmarks = yaml.safe_load(f)
            return benchmarks
        except Exception as e:
            logger.error(f"Error loading benchmarks: {e}")
            raise

    def score_ratio(self, value: float, ratio_config: Dict) -> float:
        """
        Score a single ratio value against its benchmark

        Scoring logic:
        - If within band: score = 1.0
        - If outside band: score decreases with distance from band

        Args:
            value: Actual ratio value
            ratio_config: Benchmark configuration with min, max, higher_is_better

        Returns:
            Score between 0 and 1
        """
        if pd.isna(value):
            return 0.0

        min_val = ratio_config['min']
        max_val = ratio_config['max']
        higher_is_better = ratio_config['higher_is_better']

        # Within band = perfect score
        if min_val <= value <= max_val:
            return 1.0

        # Outside band = penalty based on distance
        band_width = max_val - min_val
        band_center = (max_val + min_val) / 2

        if higher_is_better:
            if value > max_val:
                # Above ideal range - still good, slight penalty
                excess = value - max_val
                penalty = min(excess / band_width, 1.0) * 0.2  # Max 20% penalty
                return 1.0 - penalty
            else:  # value < min_val
                # Below ideal range - bad
                deficit = min_val - value
                penalty = min(deficit / band_width, 1.0)
                return max(0.0, 1.0 - penalty)
        else:  # lower is better
            if value < min_val:
                # Below ideal range - still good, slight penalty
                excess = min_val - value
                penalty = min(excess / band_width, 1.0) * 0.2
                return 1.0 - penalty
            else:  # value > max_val
                # Above ideal range - bad
                excess = value - max_val
                penalty = min(excess / band_width, 1.0)
                return max(0.0, 1.0 - penalty)

    def score_company(self, company_data: Dict, sector: str) -> Dict:
        """
        Score all ratios for a single company

        Args:
            company_data: Dictionary of ratio values
            sector: Company's sector

        Returns:
            Dictionary with individual scores and weighted total
        """
        if sector not in self.benchmarks:
            logger.warning(f"Sector '{sector}' not found in benchmarks")
            return {'total_score': 0.0, 'ratio_scores': {}}

        sector_config = self.benchmarks[sector]['ratios']
        ratio_scores = {}
        weighted_sum = 0.0
        total_weight = 0.0

        for ratio_name, ratio_config in sector_config.items():
            # Get value from company data
            value = company_data.get(ratio_name, np.nan)

            if pd.isna(value):
                logger.debug(f"{ratio_name} missing for company")
                ratio_scores[ratio_name] = {
                    'value': None,
                    'score': 0.0,
                    'benchmark_min': ratio_config['min'],
                    'benchmark_max': ratio_config['max'],
                    'weight': ratio_config['weight']
                }
                continue

            # Score the ratio
            score = self.score_ratio(value, ratio_config)
            weight = ratio_config['weight']

            ratio_scores[ratio_name] = {
                'value': value,
                'score': score,
                'benchmark_min': ratio_config['min'],
                'benchmark_max': ratio_config['max'],
                'weight': weight,
                'in_range': ratio_config['min'] <= value <= ratio_config['max']
            }

            weighted_sum += score * weight
            total_weight += weight

        # Calculate total score
        total_score = weighted_sum / total_weight if total_weight > 0 else 0.0

        return {
            'total_score': total_score,
            'ratio_scores': ratio_scores,
            'sector': sector
        }

    def normalize_within_sector(self, scores_df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize scores within each sector using z-scores

        Args:
            scores_df: DataFrame with columns: symbol, sector, total_score

        Returns:
            DataFrame with additional z_score and percentile columns
        """
        result = scores_df.copy()

        # Calculate z-scores within each sector
        def calc_zscore(group):
            if len(group) > 1:
                group['z_score'] = stats.zscore(group['total_score'])
                group['percentile'] = group['total_score'].rank(pct=True) * 100
            else:
                group['z_score'] = 0.0
                group['percentile'] = 50.0
            return group

        result = result.groupby('sector').apply(calc_zscore).reset_index(drop=True)

        return result

    def create_composite_score(self, fundamental_score: float,
                              growth_score: float,
                              risk_adjusted_score: float,
                              weights: Dict[str, float]) -> float:
        """
        Create composite score from three components

        Args:
            fundamental_score: Financial strength score (0-1)
            growth_score: Growth & efficiency score (0-1)
            risk_adjusted_score: Risk-adjusted return score (0-1)
            weights: Dictionary with keys: financial_strength,
                    growth_efficiency, risk_adjusted_return

        Returns:
            Composite score (0-100)
        """
        w_fund = weights.get('financial_strength', 0.40)
        w_growth = weights.get('growth_efficiency', 0.30)
        w_risk = weights.get('risk_adjusted_return', 0.30)

        # Ensure weights sum to 1.0
        total_weight = w_fund + w_growth + w_risk
        w_fund /= total_weight
        w_growth /= total_weight
        w_risk /= total_weight

        composite = (fundamental_score * w_fund +
                    growth_score * w_growth +
                    risk_adjusted_score * w_risk)

        return composite * 100  # Convert to 0-100 scale

    def categorize_ratios(self, sector: str) -> Dict[str, List[str]]:
        """
        Categorize ratios into financial strength vs growth/efficiency

        Args:
            sector: Sector name

        Returns:
            Dictionary with 'financial_strength' and 'growth_efficiency' lists
        """
        if sector not in self.benchmarks:
            return {'financial_strength': [], 'growth_efficiency': []}

        # Define categorization
        financial_indicators = [
            'ROE', 'ROCE', 'EBITDA_Margin', 'EBIT_Margin', 'NIM',
            'Debt_to_Equity', 'Current_Ratio', 'GNPA', 'PCR'
        ]

        growth_indicators = [
            'Revenue_Growth', 'FCF_Margin', 'Inventory_Turnover',
            'Asset_Turnover', 'Working_Capital_Days', 'Revenue_per_User',
            'Cost_to_Income'
        ]

        sector_ratios = list(self.benchmarks[sector]['ratios'].keys())

        financial_strength = [r for r in sector_ratios if r in financial_indicators]
        growth_efficiency = [r for r in sector_ratios if r in growth_indicators]

        # If ratio not categorized, put in financial strength
        uncategorized = [r for r in sector_ratios
                        if r not in financial_strength and r not in growth_efficiency]
        financial_strength.extend(uncategorized)

        return {
            'financial_strength': financial_strength,
            'growth_efficiency': growth_efficiency
        }

    def calculate_component_scores(self, ratio_scores: Dict, sector: str) -> Dict:
        """
        Calculate separate scores for financial strength and growth efficiency

        Args:
            ratio_scores: Dictionary of ratio scores from score_company
            sector: Company's sector

        Returns:
            Dictionary with financial_strength_score and growth_efficiency_score
        """
        categories = self.categorize_ratios(sector)

        # Calculate financial strength score
        fin_scores = []
        fin_weights = []
        for ratio in categories['financial_strength']:
            if ratio in ratio_scores and ratio_scores[ratio]['score'] is not None:
                fin_scores.append(ratio_scores[ratio]['score'])
                fin_weights.append(ratio_scores[ratio]['weight'])

        if fin_scores:
            financial_strength_score = np.average(fin_scores, weights=fin_weights)
        else:
            financial_strength_score = 0.0

        # Calculate growth & efficiency score
        growth_scores = []
        growth_weights = []
        for ratio in categories['growth_efficiency']:
            if ratio in ratio_scores and ratio_scores[ratio]['score'] is not None:
                growth_scores.append(ratio_scores[ratio]['score'])
                growth_weights.append(ratio_scores[ratio]['weight'])

        if growth_scores:
            growth_efficiency_score = np.average(growth_scores, weights=growth_weights)
        else:
            growth_efficiency_score = 0.0

        return {
            'financial_strength_score': financial_strength_score,
            'growth_efficiency_score': growth_efficiency_score
        }


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    # Sample company data
    sample_company = {
        'ROE': 16.5,
        'NIM': 3.2,
        'GNPA': 2.1,
        'PCR': 72.0,
        'Cost_to_Income': 42.0
    }

    scorer = RatioScorer('../sector_benchmarks.yml')
    result = scorer.score_company(sample_company, 'Banking')

    print("\nSample Scoring Result:")
    print(f"Total Score: {result['total_score']:.2f}")
    print("\nRatio Scores:")
    for ratio, details in result['ratio_scores'].items():
        print(f"  {ratio}: {details['score']:.2f} (value: {details.get('value', 'N/A')})")
