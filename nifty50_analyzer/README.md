# 📊 NIFTY 50 Stock Analyzer

A comprehensive stock analysis tool that evaluates all 50 NIFTY companies using sector-specific benchmarks, risk-adjusted returns, and generates actionable Buy/Hold/Avoid signals.

## ✨ Features

- **Precise Return Calculations**: Uses logarithmic returns with exact annualization formulas
- **Volatility Analysis**: Calculates annualized volatility (σ × √252) for risk assessment
- **Sector-Specific Benchmarking**: Evaluates companies against industry peers, not absolute standards
- **Composite Scoring**: 40% financial strength + 30% growth/efficiency + 30% risk-adjusted returns
- **Smart Signal Generation**: Buy (top 20%) / Hold (middle) / Avoid (bottom 20%) with confidence levels
- **Risk Flag Detection**: Monitors debt, profitability, volatility, NPAs, and margins
- **Beautiful Reports**: Generates HTML reports and CSV exports for easy analysis
- **One-Click Execution**: No coding required - just double-click to run!

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Required packages**: pandas, numpy, pyyaml (auto-installed by launcher)
- **Data files**: 1 year of daily price data + fundamental ratios for NIFTY 50 stocks

## 🚀 Quick Start (Non-Coders)

### Step 1: Prepare Your Data

1. **Price Data** (`inputs/prices.csv`):
   - Copy `inputs/prices_template.csv` to `inputs/prices.csv`
   - Fill with 1 year (252 trading days) of daily closing prices
   - Format: Date column + 50 stock symbol columns

2. **Fundamental Data** (`inputs/fundamentals.csv`):
   - Copy `inputs/fundamentals_template.csv` to `inputs/fundamentals.csv`
   - Fill with latest financial ratios for each company
   - Leave cells blank if ratio doesn't apply to that sector

3. **Sector Mapping** (`inputs/sector_mapping.csv`):
   - Already complete! No changes needed.
   - Maps all 50 NIFTY companies to their sectors

### Step 2: Run the Analyzer

**Windows:**
1. Double-click `run_analyzer.bat`
2. Wait for analysis to complete (1-2 minutes)
3. Check the `outputs/` folder for reports

**Mac/Linux:**
1. Double-click `run_analyzer.command`
2. If prompted, allow execution permissions
3. Wait for analysis to complete
4. Check the `outputs/` folder for reports

### Step 3: View Results

Open the HTML report in your browser for the best experience:
- `outputs/report_[timestamp].html` - Beautiful interactive report

Or open CSV files in Excel:
- `outputs/summary_[timestamp].csv` - Quick overview of all signals
- `outputs/detailed_analysis_[timestamp].csv` - Complete metrics
- `outputs/risk_flags_[timestamp].csv` - Stocks with risk concerns

## 📊 Understanding the Results

### Signals

- **🟢 BUY**: Top 20% in sector + low risk (≤1 flag)
  - *High Confidence*: No risk flags, strong fundamentals
  - *Medium Confidence*: 1 minor risk flag present

- **🟡 HOLD**: Middle 60% or mixed signals
  - Generally acceptable but not exceptional
  - Monitor for changes

- **🔴 AVOID**: Bottom 20% or high risk (≥3 flags)
  - Weak fundamentals or balance sheet stress
  - Consider avoiding or reducing exposure

### Risk Flags

The analyzer monitors 6 key risk indicators:

1. **High Volatility**: Stock in top 15% most volatile
2. **High Debt**: Debt-to-Equity > 2.0
3. **Low Profitability**: ROE < 5%
4. **High NPA** (Banks): Gross NPA > 5%
5. **Negative Returns**: Expected 1-year return < 0%
6. **Weak Margins**: EBITDA margin < 5%

### Composite Score

Companies are scored 0-100 based on:
- **40%**: Financial Strength (ROE, margins, debt levels)
- **30%**: Growth & Efficiency (revenue growth, asset turnover)
- **30%**: Risk-Adjusted Return (expected return, volatility, Sharpe ratio)

Scores are **sector-relative**, meaning a score of 85 indicates top performance *within that sector*.

## 🔧 Advanced Usage (For Coders)

### Run from Command Line

```bash
cd nifty50_analyzer/src
python main.py
```

### Customize Configuration

Edit `config.yml` to adjust:
- Signal thresholds (default: 80/20 for top/bottom 20%)
- Composite score weights (default: 40/30/30)
- Risk-free rate (default: 6.5%)
- Risk flag limits

Edit `sector_benchmarks.yml` to adjust:
- Ideal ratio ranges for each sector
- Ratio weights within categories
- Add/remove ratios for specific sectors

### Module Overview

```
src/
├── returns_risk.py    # Calculate expected returns & volatility
├── scoring.py         # Score ratios against sector benchmarks
├── signal.py          # Generate Buy/Hold/Avoid signals
├── reporting.py       # Create HTML & CSV reports
└── main.py           # Main orchestrator (run this)
```

### Import as Library

```python
from nifty50_analyzer.src.main import NIFTY50Analyzer

analyzer = NIFTY50Analyzer()
signals_df, summary = analyzer.run_complete_analysis()

# Access results programmatically
top_buys = signals_df[signals_df['signal'] == 'BUY'].head(10)
print(top_buys[['symbol', 'composite_score', 'explanation']])
```

## 📐 Methodology

### 1. Return Calculation
```
Daily Log Return = ln(P_t / P_{t-1})
Expected Annual Return = mean(daily log returns) × 252
```

### 2. Volatility Calculation
```
Daily Volatility = std(daily log returns)
Annual Volatility = daily volatility × √252
```

### 3. Sharpe Ratio
```
Sharpe Ratio = (Expected Return - Risk-Free Rate) / Volatility
```

### 4. Ratio Scoring

Each ratio is scored against sector-specific ideal ranges:
- **In Range**: Score = 1.0 (ideal)
- **Out of Range**: Score decreases with distance from range

Ratios are weighted and combined into category scores:
- Financial Strength (40%)
- Growth & Efficiency (30%)
- Risk-Adjusted Return (30%)

### 5. Percentile Ranking

Companies are ranked within their sector using z-score normalization:
```
z-score = (company_score - sector_mean) / sector_std
percentile = rank within sector
```

### 6. Signal Generation

Signals are generated based on percentile rank and risk flags:

| Percentile | Risk Flags | Signal | Confidence |
|------------|------------|--------|------------|
| ≥ 80% | 0 | BUY | HIGH |
| ≥ 80% | 1 | BUY | MEDIUM |
| ≥ 80% | ≥ 2 | HOLD | LOW |
| 20-80% | 0-2 | HOLD | MEDIUM |
| 20-80% | ≥ 3 | AVOID | MEDIUM |
| < 20% | Any | AVOID | HIGH |

## 🛡️ Data Safety Rules

**IMPORTANT**: This analyzer follows strict data quality rules:

✅ **NO Interpolation**: Missing values are NOT filled or guessed
✅ **NO Forward Fill**: Future data does NOT influence past
✅ **NO Backward Fill**: Past data does NOT influence future

If data is incomplete, the analysis will warn you. This prevents false signals from estimated data.

## 📁 Directory Structure

```
nifty50_analyzer/
├── config.yml                    # Main configuration
├── sector_benchmarks.yml         # Sector-specific ideal ranges
├── run_analyzer.bat             # Windows launcher
├── run_analyzer.command         # Mac/Linux launcher
├── README.md                    # This file
├── inputs/                      # Input data files
│   ├── prices_template.csv      # Template for price data
│   ├── fundamentals_template.csv # Template for ratios
│   ├── sector_mapping.csv       # Sector classifications (complete)
│   ├── prices.csv              # YOUR price data (you create this)
│   └── fundamentals.csv        # YOUR fundamental data (you create this)
├── outputs/                    # Generated reports
│   ├── summary_*.csv           # Signal summaries
│   ├── detailed_analysis_*.csv # Complete metrics
│   ├── risk_flags_*.csv        # Risk analysis
│   ├── report_*.html           # HTML reports
│   └── analyzer.log            # Execution logs
└── src/                        # Source code modules
    ├── main.py                 # Main orchestrator
    ├── returns_risk.py         # Returns & risk calculations
    ├── scoring.py              # Ratio scoring engine
    ├── signal.py               # Signal generator
    └── reporting.py            # Report generator
```

## ⚠️ Important Notes

1. **Data Quality**: Ensure your input data is accurate and complete
2. **Market Conditions**: Past returns do not guarantee future performance
3. **Professional Advice**: This tool is for analysis only, not financial advice
4. **Regular Updates**: Re-run analysis periodically with fresh data
5. **Sector Changes**: If NIFTY 50 composition changes, update sector_mapping.csv

## 🐛 Troubleshooting

### "Python not found"
- Install Python from https://www.python.org/downloads/
- Ensure "Add Python to PATH" is checked during installation

### "File not found" errors
- Make sure you've created `inputs/prices.csv` and `inputs/fundamentals.csv`
- Don't just rename templates - fill them with actual data

### "Insufficient data" error
- Price data must have at least 200-252 trading days
- Check for missing values in your CSV files

### "Validation failed" errors
- Ensure all 50 NIFTY companies have data in all input files
- Check that column names match templates exactly

### Analysis produces no BUY signals
- This is possible if market conditions are weak
- Review your data quality and benchmark settings
- Check if risk thresholds are too strict in config.yml

## 📞 Support

- Check `outputs/analyzer.log` for detailed error messages
- Review data templates for correct format
- Verify all 50 NIFTY symbols are present in your data

## 📜 License

This tool is provided as-is for educational and analysis purposes.

## 🎯 Disclaimer

**NOT FINANCIAL ADVICE**: This analyzer is a tool for research and education only. It does not constitute financial, investment, or trading advice. Always:
- Do your own research
- Consult qualified financial advisors
- Understand the risks before investing
- Verify all data and calculations independently

Past performance does not indicate future results. Stock markets involve risk of loss.

---

**Happy Analyzing! 📊📈**
