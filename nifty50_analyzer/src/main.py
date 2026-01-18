"""
Main Orchestrator for NIFTY 50 Stock Analyzer
One-click execution: Loads data → Analyzes → Generates reports
"""

import pandas as pd
import numpy as np
import yaml
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Tuple

# Import our modules
from returns_risk import ReturnsRiskCalculator, load_price_data
from scoring import RatioScorer
from signal import SignalGenerator
from reporting import ReportGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../outputs/analyzer.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class NIFTY50Analyzer:
    """Complete NIFTY 50 Stock Analyzer"""

    def __init__(self, config_path: str = '../config.yml',
                 benchmarks_path: str = '../sector_benchmarks.yml'):
        """
        Initialize analyzer with configuration

        Args:
            config_path: Path to main config file
            benchmarks_path: Path to sector benchmarks file
        """
        logger.info("=" * 80)
        logger.info("NIFTY 50 STOCK ANALYZER")
        logger.info("=" * 80)

        # Load configurations
        self.config = self._load_config(config_path)
        self.benchmarks = self._load_config(benchmarks_path)

        # Initialize modules
        self.returns_calculator = ReturnsRiskCalculator(
            trading_days=self.config.get('trading_days', 252)
        )
        self.scorer = RatioScorer(
            benchmarks=self.benchmarks,
            weights=self.config.get('weights', {})
        )
        self.signal_generator = SignalGenerator(
            config=self.config.get('signals', {})
        )
        self.reporter = ReportGenerator(
            output_dir='../outputs'
        )

        logger.info("✅ All modules initialized successfully")

    def _load_config(self, path: str) -> Dict:
        """Load YAML configuration file"""
        try:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"✅ Loaded config from {path}")
            return config
        except Exception as e:
            logger.error(f"❌ Failed to load config from {path}: {e}")
            raise

    def load_inputs(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Load all input files

        Returns:
            Tuple of (prices_df, fundamentals_df, sector_mapping_df)
        """
        logger.info("\n" + "=" * 80)
        logger.info("STEP 1: LOADING INPUT DATA")
        logger.info("=" * 80)

        inputs_dir = '../inputs'

        # Load price data
        logger.info("📊 Loading price data...")
        prices_df = load_price_data(f'{inputs_dir}/prices.csv')
        logger.info(f"   ✅ Loaded {len(prices_df)} days × {len(prices_df.columns)} stocks")

        # Load fundamentals
        logger.info("📈 Loading fundamentals data...")
        fundamentals_df = pd.read_csv(f'{inputs_dir}/fundamentals.csv')
        logger.info(f"   ✅ Loaded {len(fundamentals_df)} companies with fundamental ratios")

        # Load sector mapping
        logger.info("🏢 Loading sector mapping...")
        sector_mapping_df = pd.read_csv(f'{inputs_dir}/sector_mapping.csv')
        logger.info(f"   ✅ Loaded sector classification for {len(sector_mapping_df)} companies")

        # Validate data quality
        self._validate_inputs(prices_df, fundamentals_df, sector_mapping_df)

        return prices_df, fundamentals_df, sector_mapping_df

    def _validate_inputs(self, prices_df: pd.DataFrame,
                        fundamentals_df: pd.DataFrame,
                        sector_mapping_df: pd.DataFrame):
        """Validate input data quality"""
        logger.info("\n🔍 Validating data quality...")

        errors = []

        # Check for required NIFTY 50 symbols
        expected_symbols = set(self.config.get('nifty50_symbols', []))
        price_symbols = set(prices_df.columns)
        fundamental_symbols = set(fundamentals_df['Company'].values)
        sector_symbols = set(sector_mapping_df['Company'].values)

        missing_from_prices = expected_symbols - price_symbols
        missing_from_fundamentals = expected_symbols - fundamental_symbols
        missing_from_sectors = expected_symbols - sector_symbols

        if missing_from_prices:
            errors.append(f"Missing price data for: {missing_from_prices}")

        if missing_from_fundamentals:
            errors.append(f"Missing fundamentals for: {missing_from_fundamentals}")

        if missing_from_sectors:
            errors.append(f"Missing sector mapping for: {missing_from_sectors}")

        # Check data completeness
        if len(prices_df) < self.config.get('min_trading_days', 200):
            errors.append(f"Insufficient price data: {len(prices_df)} days (need ≥200)")

        # Check for excessive missing values
        allow_interpolation = self.config.get('data_quality', {}).get('allow_interpolation', False)
        if not allow_interpolation:
            null_counts = prices_df.isnull().sum()
            stocks_with_nulls = null_counts[null_counts > 0]
            if len(stocks_with_nulls) > 0:
                logger.warning(f"   ⚠️  Found missing price data in {len(stocks_with_nulls)} stocks")
                logger.warning(f"   Strategy: Will exclude days with missing data (no interpolation)")

        if errors:
            logger.error("\n❌ DATA VALIDATION FAILED:")
            for error in errors:
                logger.error(f"   • {error}")
            raise ValueError("Input data validation failed. Please fix errors above.")

        logger.info("   ✅ All validation checks passed")

    def calculate_returns_and_risk(self, prices_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate expected returns and volatility for all stocks

        Args:
            prices_df: DataFrame with price data

        Returns:
            DataFrame with return and risk metrics
        """
        logger.info("\n" + "=" * 80)
        logger.info("STEP 2: CALCULATING RETURNS & RISK")
        logger.info("=" * 80)

        risk_free_rate = self.config.get('risk_free_rate', 0.065)
        logger.info(f"📊 Using risk-free rate: {risk_free_rate*100:.2f}%")

        returns_df = self.returns_calculator.analyze_portfolio(
            prices_df,
            risk_free_rate=risk_free_rate
        )

        logger.info(f"✅ Calculated returns & risk for {len(returns_df)} stocks")
        logger.info(f"   Average expected return: {returns_df['expected_return_pct'].mean():.2f}%")
        logger.info(f"   Average volatility: {returns_df['volatility_pct'].mean():.2f}%")

        return returns_df

    def score_fundamentals(self, fundamentals_df: pd.DataFrame,
                          sector_mapping_df: pd.DataFrame) -> pd.DataFrame:
        """
        Score fundamental ratios against sector benchmarks

        Args:
            fundamentals_df: DataFrame with fundamental ratios
            sector_mapping_df: DataFrame with sector classifications

        Returns:
            DataFrame with scores
        """
        logger.info("\n" + "=" * 80)
        logger.info("STEP 3: SCORING FUNDAMENTALS")
        logger.info("=" * 80)

        # Merge sector information
        fundamentals_with_sector = fundamentals_df.merge(
            sector_mapping_df[['Company', 'Sector']],
            on='Company',
            how='left'
        )

        # Score the portfolio
        scores_df = self.scorer.score_portfolio(fundamentals_with_sector)

        logger.info(f"✅ Scored {len(scores_df)} companies against sector benchmarks")
        logger.info(f"   Average composite score: {scores_df['composite_score'].mean():.2f}")

        return scores_df

    def combine_analysis(self, returns_df: pd.DataFrame,
                        scores_df: pd.DataFrame,
                        sector_mapping_df: pd.DataFrame) -> pd.DataFrame:
        """
        Combine returns/risk analysis with fundamental scores

        Args:
            returns_df: DataFrame with returns and risk
            scores_df: DataFrame with fundamental scores
            sector_mapping_df: DataFrame with sector info

        Returns:
            Combined analysis DataFrame
        """
        logger.info("\n" + "=" * 80)
        logger.info("STEP 4: COMBINING ANALYSIS")
        logger.info("=" * 80)

        # Reset index to merge on symbol
        returns_df_reset = returns_df.reset_index()
        returns_df_reset = returns_df_reset.rename(columns={'index': 'symbol'})

        # Merge returns with scores (scores_df should have 'symbol' column)
        combined = scores_df.merge(
            returns_df_reset,
            left_on='symbol',
            right_on='symbol',
            how='inner'
        )

        # Add sector information if not already present
        if 'sector' not in combined.columns:
            sector_map = sector_mapping_df.set_index('Company')['Sector'].to_dict()
            combined['sector'] = combined['symbol'].map(sector_map)

        logger.info(f"✅ Combined analysis for {len(combined)} stocks")

        return combined

    def generate_signals(self, analysis_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate Buy/Hold/Avoid signals

        Args:
            analysis_df: Complete analysis DataFrame

        Returns:
            DataFrame with signals added
        """
        logger.info("\n" + "=" * 80)
        logger.info("STEP 5: GENERATING SIGNALS")
        logger.info("=" * 80)

        signals_df = self.signal_generator.generate_portfolio_signals(analysis_df)

        summary = self.signal_generator.generate_summary_stats(signals_df)

        logger.info("✅ Signal generation complete:")
        logger.info(f"   🟢 BUY: {summary['buy_count']} ({summary.get('buy_pct', 0):.1f}%)")
        logger.info(f"   🟡 HOLD: {summary['hold_count']} ({summary.get('hold_pct', 0):.1f}%)")
        logger.info(f"   🔴 AVOID: {summary['avoid_count']} ({summary.get('avoid_pct', 0):.1f}%)")
        logger.info(f"   ⭐ High Confidence BUYS: {summary['high_confidence_buys']}")

        return signals_df, summary

    def export_reports(self, signals_df: pd.DataFrame, summary_stats: Dict):
        """
        Export all reports (CSV and HTML)

        Args:
            signals_df: DataFrame with signals
            summary_stats: Dictionary with summary statistics
        """
        logger.info("\n" + "=" * 80)
        logger.info("STEP 6: EXPORTING REPORTS")
        logger.info("=" * 80)

        # Create outputs directory if it doesn't exist
        os.makedirs('../outputs', exist_ok=True)

        # Export summary CSV
        logger.info("📄 Generating summary CSV...")
        summary_file = self.reporter.export_summary_csv(signals_df, summary_stats)
        logger.info(f"   ✅ {summary_file}")

        # Export detailed CSV
        logger.info("📄 Generating detailed analysis CSV...")
        detailed_file = self.reporter.export_detailed_csv(signals_df)
        logger.info(f"   ✅ {detailed_file}")

        # Export risk flags CSV
        logger.info("📄 Generating risk flags CSV...")
        risk_file = self.reporter.export_risk_flags_csv(signals_df)
        if risk_file:
            logger.info(f"   ✅ {risk_file}")

        # Generate HTML report
        logger.info("📄 Generating HTML report...")
        html_file = self.reporter.generate_html_report(
            signals_df,
            summary_stats,
            self.config
        )
        logger.info(f"   ✅ {html_file}")

        logger.info("\n🎉 All reports exported successfully!")

    def run_complete_analysis(self):
        """
        Run complete end-to-end analysis

        This is the main entry point for one-click execution
        """
        try:
            # Step 1: Load inputs
            prices_df, fundamentals_df, sector_mapping_df = self.load_inputs()

            # Step 2: Calculate returns and risk
            returns_df = self.calculate_returns_and_risk(prices_df)

            # Step 3: Score fundamentals
            scores_df = self.score_fundamentals(fundamentals_df, sector_mapping_df)

            # Step 4: Combine analysis
            analysis_df = self.combine_analysis(returns_df, scores_df, sector_mapping_df)

            # Step 5: Generate signals
            signals_df, summary_stats = self.generate_signals(analysis_df)

            # Step 6: Export reports
            self.export_reports(signals_df, summary_stats)

            logger.info("\n" + "=" * 80)
            logger.info("✅ ANALYSIS COMPLETE!")
            logger.info("=" * 80)
            logger.info("\n📂 Check the 'outputs' folder for:")
            logger.info("   • summary_*.csv - Quick overview of all signals")
            logger.info("   • detailed_analysis_*.csv - Complete metrics for all stocks")
            logger.info("   • risk_flags_*.csv - Stocks with risk concerns")
            logger.info("   • report_*.html - Beautiful HTML report (open in browser)")
            logger.info("\n💡 TIP: Open the HTML report for the best viewing experience!")

            return signals_df, summary_stats

        except Exception as e:
            logger.error(f"\n❌ ANALYSIS FAILED: {e}")
            logger.exception("Full error traceback:")
            raise


def main():
    """Main entry point"""
    print("\n" + "=" * 80)
    print("🚀 NIFTY 50 STOCK ANALYZER - Starting Analysis...")
    print("=" * 80 + "\n")

    try:
        # Check if we're in the right directory
        if not os.path.exists('../config.yml'):
            print("❌ ERROR: config.yml not found!")
            print("Please run this script from the nifty50_analyzer/src/ directory")
            print("\nExample:")
            print("  cd nifty50_analyzer/src")
            print("  python main.py")
            sys.exit(1)

        # Check if input files exist
        required_files = [
            '../inputs/prices.csv',
            '../inputs/fundamentals.csv',
            '../inputs/sector_mapping.csv'
        ]

        missing_files = [f for f in required_files if not os.path.exists(f)]
        if missing_files:
            print("❌ ERROR: Required input files not found:")
            for f in missing_files:
                print(f"   • {f}")
            print("\nPlease fill in the template files with your data:")
            print("   1. Copy prices_template.csv to prices.csv and fill with 1 year price data")
            print("   2. Copy fundamentals_template.csv to fundamentals.csv and fill with ratios")
            print("   3. sector_mapping.csv is already complete (use as-is)")
            sys.exit(1)

        # Run analysis
        analyzer = NIFTY50Analyzer()
        signals_df, summary_stats = analyzer.run_complete_analysis()

        print("\n" + "=" * 80)
        print("✅ SUCCESS! Analysis completed.")
        print("=" * 80)

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        return 1

    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        print("\nCheck analyzer.log in the outputs folder for details")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
