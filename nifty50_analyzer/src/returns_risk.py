"""
Returns and Risk Calculations for NIFTY 50 Analyzer
Calculates Expected Return and Volatility from price data
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class ReturnsRiskCalculator:
    """Calculate expected returns and volatility for stocks"""

    def __init__(self, trading_days: int = 252):
        """
        Initialize calculator

        Args:
            trading_days: Number of trading days per year (default: 252)
        """
        self.trading_days = trading_days
        self.annual_factor = np.sqrt(trading_days)

    def calculate_log_returns(self, prices: pd.Series) -> pd.Series:
        """
        Calculate logarithmic returns from price series

        Args:
            prices: Series of daily closing prices

        Returns:
            Series of log returns
        """
        # Remove any NaN values
        prices_clean = prices.dropna()

        if len(prices_clean) < 2:
            logger.warning(f"Insufficient price data: only {len(prices_clean)} points")
            return pd.Series(dtype=float)

        # Calculate log returns: ln(P_t / P_t-1)
        log_returns = np.log(prices_clean / prices_clean.shift(1))

        return log_returns.dropna()

    def calculate_expected_return(self, log_returns: pd.Series) -> float:
        """
        Calculate annualized expected return

        Formula: mean(daily log returns) × 252

        Args:
            log_returns: Series of daily log returns

        Returns:
            Annualized expected return as decimal (e.g., 0.15 = 15%)
        """
        if len(log_returns) == 0:
            return np.nan

        mean_daily_return = log_returns.mean()
        annual_return = mean_daily_return * self.trading_days

        return annual_return

    def calculate_volatility(self, log_returns: pd.Series) -> float:
        """
        Calculate annualized volatility (standard deviation)

        Formula: std(daily log returns) × √252

        Args:
            log_returns: Series of daily log returns

        Returns:
            Annualized volatility as decimal (e.g., 0.25 = 25%)
        """
        if len(log_returns) == 0:
            return np.nan

        daily_std = log_returns.std()
        annual_volatility = daily_std * self.annual_factor

        return annual_volatility

    def calculate_sharpe_ratio(self, expected_return: float,
                              volatility: float,
                              risk_free_rate: float = 0.065) -> float:
        """
        Calculate Sharpe Ratio

        Args:
            expected_return: Annual expected return (decimal)
            volatility: Annual volatility (decimal)
            risk_free_rate: Risk-free rate (decimal, default: 6.5%)

        Returns:
            Sharpe ratio
        """
        if volatility == 0 or np.isnan(volatility):
            return np.nan

        excess_return = expected_return - risk_free_rate
        sharpe = excess_return / volatility

        return sharpe

    def analyze_stock(self, prices: pd.Series,
                     risk_free_rate: float = 0.065) -> Dict[str, float]:
        """
        Complete analysis for a single stock

        Args:
            prices: Series of daily closing prices
            risk_free_rate: Risk-free rate for Sharpe ratio

        Returns:
            Dictionary with return, volatility, and Sharpe ratio
        """
        # Calculate log returns
        log_returns = self.calculate_log_returns(prices)

        if len(log_returns) == 0:
            return {
                'expected_return': np.nan,
                'volatility': np.nan,
                'sharpe_ratio': np.nan,
                'data_points': 0
            }

        # Calculate metrics
        expected_return = self.calculate_expected_return(log_returns)
        volatility = self.calculate_volatility(log_returns)
        sharpe = self.calculate_sharpe_ratio(expected_return, volatility, risk_free_rate)

        return {
            'expected_return': expected_return,
            'expected_return_pct': expected_return * 100,  # As percentage
            'volatility': volatility,
            'volatility_pct': volatility * 100,  # As percentage
            'sharpe_ratio': sharpe,
            'data_points': len(log_returns)
        }

    def analyze_portfolio(self, prices_df: pd.DataFrame,
                         risk_free_rate: float = 0.065) -> pd.DataFrame:
        """
        Analyze all stocks in the portfolio

        Args:
            prices_df: DataFrame with Date index and stock symbols as columns
            risk_free_rate: Risk-free rate for Sharpe ratio

        Returns:
            DataFrame with analysis results for all stocks
        """
        results = []

        for symbol in prices_df.columns:
            if symbol == 'Date':
                continue

            logger.info(f"Analyzing {symbol}...")

            prices = prices_df[symbol]
            analysis = self.analyze_stock(prices, risk_free_rate)
            analysis['symbol'] = symbol

            results.append(analysis)

        results_df = pd.DataFrame(results)

        # Set symbol as index
        if 'symbol' in results_df.columns:
            results_df = results_df.set_index('symbol')

        return results_df

    def validate_data_quality(self, prices: pd.Series,
                             min_completeness: float = 0.9) -> Tuple[bool, str]:
        """
        Validate data quality for a price series

        Args:
            prices: Series of prices
            min_completeness: Minimum required completeness (0.9 = 90%)

        Returns:
            Tuple of (is_valid, message)
        """
        total_points = len(prices)
        non_null_points = prices.count()

        if total_points == 0:
            return False, "No price data available"

        completeness = non_null_points / total_points

        if completeness < min_completeness:
            return False, f"Data only {completeness*100:.1f}% complete (minimum: {min_completeness*100}%)"

        # Check for consecutive missing values
        null_runs = prices.isnull().astype(int).groupby(prices.notnull().cumsum()).sum()
        max_consecutive_nulls = null_runs.max() if len(null_runs) > 0 else 0

        if max_consecutive_nulls > 10:
            return False, f"Found {max_consecutive_nulls} consecutive missing values"

        return True, "Data quality OK"


def load_price_data(file_path: str) -> pd.DataFrame:
    """
    Load price data from CSV file

    Args:
        file_path: Path to CSV file

    Returns:
        DataFrame with Date index and stock prices
    """
    logger.info(f"Loading price data from {file_path}")

    try:
        df = pd.read_csv(file_path)

        # Convert Date column to datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.set_index('Date')

        # Sort by date
        df = df.sort_index()

        logger.info(f"Loaded {len(df)} days of data for {len(df.columns)} stocks")

        return df

    except Exception as e:
        logger.error(f"Error loading price data: {e}")
        raise


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    # Create sample data
    dates = pd.date_range('2023-01-01', periods=252, freq='B')
    sample_prices = pd.DataFrame({
        'Date': dates,
        'RELIANCE': np.random.normal(2500, 50, 252).cumsum() / 252 + 2500,
        'TCS': np.random.normal(3800, 60, 252).cumsum() / 252 + 3800,
    })
    sample_prices = sample_prices.set_index('Date')

    # Calculate returns and risk
    calculator = ReturnsRiskCalculator()
    results = calculator.analyze_portfolio(sample_prices)

    print("\nSample Analysis Results:")
    print(results)
