"""
Reporting Module for NIFTY 50 Analyzer
Generates HTML reports and CSV exports
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate comprehensive reports in CSV and HTML formats"""

    def __init__(self, output_dir: str = 'outputs'):
        """
        Initialize report generator

        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir

    def export_summary_csv(self, signals_df: pd.DataFrame, summary_stats: Dict) -> str:
        """
        Export summary CSV with key metrics

        Args:
            signals_df: DataFrame with all signals
            summary_stats: Dictionary with summary statistics

        Returns:
            Path to saved file
        """
        # Select key columns for summary
        summary_cols = [
            'symbol', 'sector', 'signal', 'confidence',
            'composite_score', 'percentile', 'risk_count',
            'expected_return_pct', 'volatility_pct', 'sharpe_ratio',
            'explanation'
        ]

        # Filter to available columns
        available_cols = [col for col in summary_cols if col in signals_df.columns]
        summary_df = signals_df[available_cols].copy()

        # Sort by signal priority (BUY first) then by composite score
        signal_order = {'BUY': 0, 'HOLD': 1, 'AVOID': 2}
        summary_df['_sort_key'] = summary_df['signal'].map(signal_order)
        summary_df = summary_df.sort_values(['_sort_key', 'composite_score'], ascending=[True, False])
        summary_df = summary_df.drop('_sort_key', axis=1)

        # Save CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{self.output_dir}/summary_{timestamp}.csv'
        summary_df.to_csv(filename, index=False)

        logger.info(f"Summary CSV saved to {filename}")
        return filename

    def export_detailed_csv(self, analysis_df: pd.DataFrame) -> str:
        """
        Export detailed analysis with all metrics

        Args:
            analysis_df: Complete analysis DataFrame

        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{self.output_dir}/detailed_analysis_{timestamp}.csv'
        analysis_df.to_csv(filename, index=False)

        logger.info(f"Detailed analysis CSV saved to {filename}")
        return filename

    def export_risk_flags_csv(self, signals_df: pd.DataFrame) -> str:
        """
        Export risk flags analysis

        Args:
            signals_df: DataFrame with signals and risk flags

        Returns:
            Path to saved file
        """
        risk_data = []

        for idx, row in signals_df.iterrows():
            symbol = row.get('symbol', idx)
            risk_flags = row.get('risk_flags', {})

            if isinstance(risk_flags, dict):
                for flag_name, is_active in risk_flags.items():
                    if is_active:
                        risk_data.append({
                            'symbol': symbol,
                            'sector': row.get('sector', ''),
                            'risk_flag': flag_name.replace('_', ' ').title(),
                            'signal': row.get('signal', ''),
                            'composite_score': row.get('composite_score', 0)
                        })

        if not risk_data:
            logger.info("No risk flags detected in portfolio")
            return None

        risk_df = pd.DataFrame(risk_data)
        risk_df = risk_df.sort_values(['risk_flag', 'composite_score'], ascending=[True, False])

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{self.output_dir}/risk_flags_{timestamp}.csv'
        risk_df.to_csv(filename, index=False)

        logger.info(f"Risk flags CSV saved to {filename}")
        return filename

    def generate_html_report(self, signals_df: pd.DataFrame,
                           summary_stats: Dict,
                           config: Dict) -> str:
        """
        Generate comprehensive HTML report

        Args:
            signals_df: DataFrame with all signals
            summary_stats: Dictionary with summary statistics
            config: Configuration dictionary

        Returns:
            Path to saved HTML file
        """
        html = self._build_html_structure(signals_df, summary_stats, config)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{self.output_dir}/report_{timestamp}.html'

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        logger.info(f"HTML report saved to {filename}")
        return filename

    def _build_html_structure(self, signals_df: pd.DataFrame,
                              summary_stats: Dict,
                              config: Dict) -> str:
        """Build complete HTML report structure"""

        timestamp = datetime.now().strftime('%B %d, %Y at %I:%M %p')

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NIFTY 50 Stock Analysis Report</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 NIFTY 50 Stock Analysis Report</h1>
            <p class="timestamp">Generated on {timestamp}</p>
        </header>

        {self._build_summary_section(summary_stats)}
        {self._build_top_picks_section(signals_df)}
        {self._build_signals_by_sector_section(signals_df)}
        {self._build_detailed_table(signals_df)}
        {self._build_methodology_section(config)}

        <footer>
            <p>⚠️ <strong>Disclaimer:</strong> This report is for informational purposes only.
            Not financial advice. Always do your own research and consult a qualified financial advisor
            before making investment decisions.</p>
        </footer>
    </div>
</body>
</html>"""

        return html

    def _get_css_styles(self) -> str:
        """CSS styles for HTML report"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }

        .timestamp {
            opacity: 0.9;
            font-size: 0.95rem;
        }

        .section {
            padding: 40px;
            border-bottom: 1px solid #eee;
        }

        .section:last-of-type {
            border-bottom: none;
        }

        h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8rem;
        }

        h3 {
            color: #555;
            margin: 20px 0 10px;
            font-size: 1.3rem;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .stat-label {
            color: #666;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #333;
        }

        .stock-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .stock-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .symbol {
            font-size: 1.3rem;
            font-weight: bold;
            color: #333;
        }

        .badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
            text-transform: uppercase;
        }

        .badge-buy {
            background: #d4edda;
            color: #155724;
        }

        .badge-hold {
            background: #fff3cd;
            color: #856404;
        }

        .badge-avoid {
            background: #f8d7da;
            color: #721c24;
        }

        .confidence {
            font-size: 0.9rem;
            color: #666;
            margin-left: 10px;
        }

        .explanation {
            color: #555;
            font-size: 0.95rem;
            margin: 10px 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.9rem;
        }

        th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid #eee;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .methodology {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }

        .methodology ul {
            margin-left: 20px;
            margin-top: 10px;
        }

        .methodology li {
            margin: 8px 0;
        }

        footer {
            background: #f8f9fa;
            padding: 30px 40px;
            text-align: center;
            color: #666;
        }

        .sector-stats {
            margin: 20px 0;
        }

        .sector-bar {
            margin: 15px 0;
        }

        .sector-name {
            font-weight: 600;
            margin-bottom: 5px;
            color: #555;
        }

        .bar-container {
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            height: 30px;
            position: relative;
        }

        .bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s;
            display: flex;
            align-items: center;
            padding: 0 10px;
            color: white;
            font-weight: bold;
            font-size: 0.85rem;
        }
        """

    def _build_summary_section(self, summary_stats: Dict) -> str:
        """Build summary statistics section"""
        total = summary_stats.get('total_stocks', 0)
        buy_count = summary_stats.get('buy_count', 0)
        hold_count = summary_stats.get('hold_count', 0)
        avoid_count = summary_stats.get('avoid_count', 0)
        high_conf_buys = summary_stats.get('high_confidence_buys', 0)
        avg_score = summary_stats.get('avg_composite_score', 0)

        return f"""
        <section class="section">
            <h2>📈 Executive Summary</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Total Stocks</div>
                    <div class="stat-value">{total}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Buy Signals</div>
                    <div class="stat-value" style="color: #28a745;">{buy_count}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Hold Signals</div>
                    <div class="stat-value" style="color: #ffc107;">{hold_count}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Avoid Signals</div>
                    <div class="stat-value" style="color: #dc3545;">{avoid_count}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">High Conviction Buys</div>
                    <div class="stat-value" style="color: #155724;">⭐ {high_conf_buys}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Avg Composite Score</div>
                    <div class="stat-value">{avg_score:.1f}</div>
                </div>
            </div>
        </section>
        """

    def _build_top_picks_section(self, signals_df: pd.DataFrame) -> str:
        """Build top stock picks section"""
        buys = signals_df[signals_df['signal'] == 'BUY'].copy()
        buys = buys.sort_values('composite_score', ascending=False).head(10)

        if len(buys) == 0:
            return """
            <section class="section">
                <h2>⭐ Top Stock Picks</h2>
                <p>No BUY signals generated in current analysis.</p>
            </section>
            """

        cards_html = ""
        for idx, row in buys.iterrows():
            symbol = row.get('symbol', idx)
            sector = row.get('sector', 'N/A')
            score = row.get('composite_score', 0)
            confidence = row.get('confidence', 'MEDIUM')
            explanation = row.get('explanation', 'No explanation available')
            exp_return = row.get('expected_return_pct', 0)
            volatility = row.get('volatility_pct', 0)

            cards_html += f"""
            <div class="stock-card">
                <div class="stock-header">
                    <div>
                        <span class="symbol">{symbol}</span>
                        <span class="confidence">({confidence} confidence)</span>
                    </div>
                    <span class="badge badge-buy">BUY</span>
                </div>
                <div style="color: #666; margin: 5px 0;">
                    <strong>Sector:</strong> {sector} |
                    <strong>Score:</strong> {score:.1f} |
                    <strong>Exp. Return:</strong> {exp_return:.1f}% |
                    <strong>Volatility:</strong> {volatility:.1f}%
                </div>
                <div class="explanation">{explanation}</div>
            </div>
            """

        return f"""
        <section class="section">
            <h2>⭐ Top Stock Picks (BUY Signals)</h2>
            {cards_html}
        </section>
        """

    def _build_signals_by_sector_section(self, signals_df: pd.DataFrame) -> str:
        """Build signals breakdown by sector"""
        if 'sector' not in signals_df.columns:
            return ""

        sector_summary = signals_df.groupby('sector')['signal'].value_counts().unstack(fill_value=0)

        bars_html = ""
        for sector in sector_summary.index:
            buy_count = sector_summary.loc[sector].get('BUY', 0)
            hold_count = sector_summary.loc[sector].get('HOLD', 0)
            avoid_count = sector_summary.loc[sector].get('AVOID', 0)
            total = buy_count + hold_count + avoid_count

            buy_pct = (buy_count / total * 100) if total > 0 else 0

            bars_html += f"""
            <div class="sector-bar">
                <div class="sector-name">{sector}</div>
                <div class="bar-container">
                    <div class="bar-fill" style="width: {buy_pct}%;">
                        {buy_count} BUY | {hold_count} HOLD | {avoid_count} AVOID
                    </div>
                </div>
            </div>
            """

        return f"""
        <section class="section">
            <h2>🏢 Signals by Sector</h2>
            <div class="sector-stats">
                {bars_html}
            </div>
        </section>
        """

    def _build_detailed_table(self, signals_df: pd.DataFrame) -> str:
        """Build detailed results table"""
        # Sort by signal priority and score
        signal_order = {'BUY': 0, 'HOLD': 1, 'AVOID': 2}
        df_sorted = signals_df.copy()
        df_sorted['_sort'] = df_sorted['signal'].map(signal_order)
        df_sorted = df_sorted.sort_values(['_sort', 'composite_score'], ascending=[True, False])

        rows_html = ""
        for idx, row in df_sorted.iterrows():
            symbol = row.get('symbol', idx)
            sector = row.get('sector', 'N/A')
            signal = row.get('signal', 'HOLD')
            confidence = row.get('confidence', 'MEDIUM')
            score = row.get('composite_score', 0)
            percentile = row.get('percentile', 50)
            risk_count = row.get('risk_count', 0)

            signal_class = f"badge-{signal.lower()}"

            rows_html += f"""
            <tr>
                <td><strong>{symbol}</strong></td>
                <td>{sector}</td>
                <td><span class="badge {signal_class}">{signal}</span></td>
                <td>{confidence}</td>
                <td>{score:.1f}</td>
                <td>{percentile:.0f}%</td>
                <td>{'⚠️ ' * risk_count if risk_count > 0 else '✅'} {risk_count}</td>
            </tr>
            """

        return f"""
        <section class="section">
            <h2>📋 Complete Analysis Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Sector</th>
                        <th>Signal</th>
                        <th>Confidence</th>
                        <th>Score</th>
                        <th>Percentile</th>
                        <th>Risk Flags</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </section>
        """

    def _build_methodology_section(self, config: Dict) -> str:
        """Build methodology explanation section"""
        buy_threshold = config.get('signals', {}).get('buy_threshold', 80)
        avoid_threshold = config.get('signals', {}).get('avoid_threshold', 20)

        weights = config.get('weights', {})
        financial = weights.get('financial_strength', 40) * 100
        growth = weights.get('growth_efficiency', 30) * 100
        risk_return = weights.get('risk_adjusted_return', 30) * 100

        return f"""
        <section class="section">
            <h2>📚 Methodology</h2>
            <div class="methodology">
                <h3>Analysis Framework</h3>
                <ul>
                    <li><strong>Data Period:</strong> 1 year (252 trading days)</li>
                    <li><strong>Return Calculation:</strong> Log returns annualized (mean × 252)</li>
                    <li><strong>Volatility:</strong> Standard deviation × √252</li>
                    <li><strong>Sector Benchmarking:</strong> Companies scored against sector-specific ideal ranges</li>
                </ul>

                <h3>Composite Score Weighting</h3>
                <ul>
                    <li><strong>Financial Strength:</strong> {financial:.0f}% (ROE, margins, debt levels)</li>
                    <li><strong>Growth & Efficiency:</strong> {growth:.0f}% (revenue growth, asset turnover)</li>
                    <li><strong>Risk-Adjusted Return:</strong> {risk_return:.0f}% (expected return, volatility, Sharpe ratio)</li>
                </ul>

                <h3>Signal Generation Logic</h3>
                <ul>
                    <li><strong>BUY:</strong> Top {100-buy_threshold}% in sector + low risk flags (≤1)</li>
                    <li><strong>HOLD:</strong> Middle range OR mixed signals</li>
                    <li><strong>AVOID:</strong> Bottom {avoid_threshold}% OR high risk (≥3 flags)</li>
                </ul>

                <h3>Risk Flags Monitored</h3>
                <ul>
                    <li>High volatility (top 15%)</li>
                    <li>Excessive debt (D/E > 2.0)</li>
                    <li>Low profitability (ROE < 5%)</li>
                    <li>High NPAs for banks (GNPA > 5%)</li>
                    <li>Negative expected returns</li>
                    <li>Weak margins (EBITDA < 5%)</li>
                </ul>
            </div>
        </section>
        """


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    # Sample data for testing
    sample_data = pd.DataFrame({
        'symbol': ['HDFCBANK', 'RELIANCE', 'TCS'],
        'sector': ['Banking', 'Energy', 'IT'],
        'signal': ['BUY', 'HOLD', 'BUY'],
        'confidence': ['HIGH', 'MEDIUM', 'MEDIUM'],
        'composite_score': [85.2, 65.0, 78.5],
        'percentile': [88, 55, 82],
        'risk_count': [0, 1, 1],
        'expected_return_pct': [15.2, 10.5, 18.3],
        'volatility_pct': [22.5, 28.0, 20.1],
        'sharpe_ratio': [0.65, 0.35, 0.85],
        'explanation': ['Top 12% in sector | No risk flags detected',
                       'Mid-range performance (percentile: 55) | 1 risk flag(s): High Volatility',
                       'Top 18% in sector | Minor concern: High Debt']
    })

    sample_stats = {
        'total_stocks': 50,
        'buy_count': 12,
        'hold_count': 28,
        'avoid_count': 10,
        'high_confidence_buys': 8,
        'avg_composite_score': 62.5
    }

    config = {
        'signals': {'buy_threshold': 80, 'avoid_threshold': 20},
        'weights': {'financial_strength': 0.40, 'growth_efficiency': 0.30, 'risk_adjusted_return': 0.30}
    }

    reporter = ReportGenerator(output_dir='../outputs')

    # Generate reports
    print("\nGenerating reports...")
    html_file = reporter.generate_html_report(sample_data, sample_stats, config)
    print(f"HTML report: {html_file}")
