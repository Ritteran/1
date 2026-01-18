"""
Signal Generation Module for NIFTY 50 Analyzer
Generates Buy / Hold / Avoid signals based on composite scores and risk flags
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class SignalGenerator:
    """Generate investment signals (Buy/Hold/Avoid) with explanations"""

    def __init__(self, config: Dict):
        """
        Initialize signal generator

        Args:
            config: Configuration dictionary with signal thresholds and risk limits
        """
        self.buy_threshold = config.get('buy_threshold', 80)  # Top 20%
        self.avoid_threshold = config.get('avoid_threshold', 20)  # Bottom 20%

        # Risk flag thresholds
        self.max_volatility_percentile = config.get('max_volatility_percentile', 85)
        self.max_debt_to_equity = config.get('max_debt_to_equity', 2.0)
        self.min_roe = config.get('min_roe', 5.0)
        self.max_gnpa = config.get('max_gnpa', 5.0)  # For banks

    def check_risk_flags(self, company_data: Dict) -> Dict[str, bool]:
        """
        Check for risk flags that should downgrade signals

        Args:
            company_data: Dictionary with company metrics

        Returns:
            Dictionary of risk flags (True = risk detected)
        """
        flags = {}

        # High volatility flag
        volatility_pct = company_data.get('volatility_percentile', 50)
        flags['high_volatility'] = volatility_pct >= self.max_volatility_percentile

        # High debt flag
        debt_to_equity = company_data.get('Debt_to_Equity', 0.0)
        if not pd.isna(debt_to_equity):
            flags['high_debt'] = debt_to_equity > self.max_debt_to_equity
        else:
            flags['high_debt'] = False

        # Low profitability flag
        roe = company_data.get('ROE', 100.0)  # Default high if missing
        if not pd.isna(roe):
            flags['low_profitability'] = roe < self.min_roe
        else:
            flags['low_profitability'] = False

        # High NPA flag (for banks)
        sector = company_data.get('sector', '')
        if sector == 'Banking':
            gnpa = company_data.get('GNPA', 0.0)
            if not pd.isna(gnpa):
                flags['high_npa'] = gnpa > self.max_gnpa
            else:
                flags['high_npa'] = False
        else:
            flags['high_npa'] = False

        # Negative expected return flag
        expected_return = company_data.get('expected_return_pct', 0.0)
        if not pd.isna(expected_return):
            flags['negative_return'] = expected_return < 0
        else:
            flags['negative_return'] = False

        # Weak margins flag (sector-specific)
        ebitda_margin = company_data.get('EBITDA_Margin', 100.0)
        if not pd.isna(ebitda_margin):
            # Very low margins
            flags['weak_margins'] = ebitda_margin < 5.0
        else:
            flags['weak_margins'] = False

        return flags

    def count_risk_flags(self, risk_flags: Dict[str, bool]) -> int:
        """Count number of active risk flags"""
        return sum(1 for flag in risk_flags.values() if flag)

    def generate_signal(self, company_data: Dict) -> Dict:
        """
        Generate Buy/Hold/Avoid signal for a company

        Signal Logic:
        - Buy: Composite score in top 20% of sector AND low risk flags (≤1)
        - Hold: Middle range OR mixed signals (good score but some risks)
        - Avoid: Bottom 20% OR balance sheet stress (≥3 risk flags)

        Args:
            company_data: Dictionary with all company metrics

        Returns:
            Dictionary with signal, confidence, and reasoning
        """
        percentile = company_data.get('percentile', 50)
        composite_score = company_data.get('composite_score', 50)
        risk_flags = self.check_risk_flags(company_data)
        risk_count = self.count_risk_flags(risk_flags)

        # Determine base signal from percentile
        if percentile >= self.buy_threshold:
            base_signal = 'BUY'
        elif percentile <= self.avoid_threshold:
            base_signal = 'AVOID'
        else:
            base_signal = 'HOLD'

        # Adjust signal based on risk flags
        final_signal = base_signal
        confidence = 'HIGH'
        reasons = []

        # Top performers with low risk = Strong Buy
        if base_signal == 'BUY':
            if risk_count == 0:
                final_signal = 'BUY'
                confidence = 'HIGH'
                reasons.append(f"Top {100 - percentile:.0f}% in sector")
                reasons.append("No risk flags detected")
            elif risk_count == 1:
                final_signal = 'BUY'
                confidence = 'MEDIUM'
                reasons.append(f"Top {100 - percentile:.0f}% in sector")
                reasons.append(f"Minor concern: {self._get_flag_description(risk_flags)}")
            else:  # risk_count >= 2
                final_signal = 'HOLD'
                confidence = 'LOW'
                reasons.append(f"Good fundamentals (top {100 - percentile:.0f}%)")
                reasons.append(f"BUT {risk_count} risk flags: {self._get_flag_description(risk_flags)}")

        # Middle range = Hold (unless severe risks)
        elif base_signal == 'HOLD':
            if risk_count >= 3:
                final_signal = 'AVOID'
                confidence = 'MEDIUM'
                reasons.append(f"Multiple risks detected ({risk_count} flags)")
                reasons.append(self._get_flag_description(risk_flags))
            else:
                final_signal = 'HOLD'
                confidence = 'MEDIUM' if risk_count == 0 else 'LOW'
                reasons.append(f"Mid-range performance (percentile: {percentile:.0f})")
                if risk_count > 0:
                    reasons.append(f"{risk_count} risk flag(s): {self._get_flag_description(risk_flags)}")

        # Weak performers = Avoid
        elif base_signal == 'AVOID':
            final_signal = 'AVOID'
            if risk_count >= 2:
                confidence = 'HIGH'
                reasons.append(f"Weak fundamentals (bottom {percentile:.0f}%)")
                reasons.append(f"Multiple risks: {self._get_flag_description(risk_flags)}")
            else:
                confidence = 'MEDIUM'
                reasons.append(f"Below average performance (bottom {percentile:.0f}%)")
                if risk_count > 0:
                    reasons.append(f"Risk detected: {self._get_flag_description(risk_flags)}")

        return {
            'signal': final_signal,
            'confidence': confidence,
            'composite_score': composite_score,
            'percentile': percentile,
            'risk_flags': risk_flags,
            'risk_count': risk_count,
            'reasons': reasons,
            'explanation': ' | '.join(reasons)
        }

    def _get_flag_description(self, risk_flags: Dict[str, bool]) -> str:
        """Convert risk flags to readable description"""
        active_flags = [flag.replace('_', ' ').title()
                       for flag, is_active in risk_flags.items()
                       if is_active]

        if not active_flags:
            return "None"

        return ', '.join(active_flags)

    def generate_portfolio_signals(self, analysis_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate signals for entire portfolio

        Args:
            analysis_df: DataFrame with all company metrics

        Returns:
            DataFrame with signal, confidence, and reasoning columns added
        """
        signals = []

        for idx, row in analysis_df.iterrows():
            company_data = row.to_dict()
            signal_result = self.generate_signal(company_data)

            signals.append({
                'symbol': row.get('symbol', idx),
                'signal': signal_result['signal'],
                'confidence': signal_result['confidence'],
                'composite_score': signal_result['composite_score'],
                'percentile': signal_result['percentile'],
                'risk_count': signal_result['risk_count'],
                'explanation': signal_result['explanation'],
                'risk_flags': signal_result['risk_flags']
            })

        signals_df = pd.DataFrame(signals)

        # Merge with original data
        result = analysis_df.copy()
        for col in ['signal', 'confidence', 'explanation', 'risk_count']:
            if col in signals_df.columns:
                result[col] = signals_df[col].values

        return result

    def get_top_picks(self, signals_df: pd.DataFrame, count: int = 10) -> pd.DataFrame:
        """
        Get top stock picks (highest conviction buys)

        Args:
            signals_df: DataFrame with signals
            count: Number of top picks to return

        Returns:
            DataFrame with top picks sorted by score
        """
        # Filter to BUY signals only
        buys = signals_df[signals_df['signal'] == 'BUY'].copy()

        # Sort by composite score descending
        buys = buys.sort_values('composite_score', ascending=False)

        return buys.head(count)

    def generate_summary_stats(self, signals_df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics for the signals

        Args:
            signals_df: DataFrame with signals

        Returns:
            Dictionary with summary statistics
        """
        total = len(signals_df)

        summary = {
            'total_stocks': total,
            'buy_count': len(signals_df[signals_df['signal'] == 'BUY']),
            'hold_count': len(signals_df[signals_df['signal'] == 'HOLD']),
            'avoid_count': len(signals_df[signals_df['signal'] == 'AVOID']),
            'high_confidence_buys': len(signals_df[
                (signals_df['signal'] == 'BUY') & (signals_df['confidence'] == 'HIGH')
            ]),
            'stocks_with_risks': len(signals_df[signals_df['risk_count'] > 0]),
            'avg_composite_score': signals_df['composite_score'].mean(),
        }

        # Add percentages
        if total > 0:
            summary['buy_pct'] = (summary['buy_count'] / total) * 100
            summary['hold_pct'] = (summary['hold_count'] / total) * 100
            summary['avoid_pct'] = (summary['avoid_count'] / total) * 100

        return summary


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    # Sample company data
    sample_data = {
        'symbol': 'HDFCBANK',
        'sector': 'Banking',
        'percentile': 85,
        'composite_score': 78.5,
        'volatility_percentile': 45,
        'Debt_to_Equity': 0.25,
        'ROE': 16.5,
        'GNPA': 2.1,
        'expected_return_pct': 12.5
    }

    config = {
        'buy_threshold': 80,
        'avoid_threshold': 20,
        'max_volatility_percentile': 85,
        'max_debt_to_equity': 2.0,
        'min_roe': 5.0,
        'max_gnpa': 5.0
    }

    generator = SignalGenerator(config)
    signal = generator.generate_signal(sample_data)

    print("\nSample Signal:")
    print(f"Signal: {signal['signal']}")
    print(f"Confidence: {signal['confidence']}")
    print(f"Explanation: {signal['explanation']}")
    print(f"Risk Flags: {signal['risk_count']}")
