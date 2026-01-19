#!/usr/bin/env python3
"""
Demo script for NSE Equity Securities Scraper
Shows how to fetch and work with instruments data from NSE India
"""

import json
from nse_scraper import NSEScraper

def main():
    print("=" * 80)
    print("NSE EQUITY SECURITIES SCRAPER - DEMO")
    print("=" * 80)
    print()
    print("This script demonstrates how to fetch instruments/securities data from NSE")
    print()

    # Initialize scraper
    scraper = NSEScraper()

    # Method 1: Fetch Equity Securities
    print("📊 Method 1: Fetch All Equity Securities")
    print("-" * 80)
    print("Usage: scraper.scrape_equity_securities()")
    print()
    print("This fetches the complete list of equity securities traded on NSE.")
    print("Each security includes:")
    print("  - Symbol (e.g., HDFCBANK, RELIANCE)")
    print("  - Company Name")
    print("  - Industry/Sector")
    print("  - ISIN Number")
    print("  - Last Price, Change, % Change")
    print("  - Previous Close, Open, High, Low")
    print("  - 52-week High/Low")
    print()

    try:
        print("Fetching securities data...")
        securities = scraper.scrape_equity_securities()

        if securities:
            print(f"✅ Successfully fetched {len(securities)} securities!")
            print()

            # Save to JSON
            scraper.save_to_file(securities, 'nse_equity_securities.json', 'json')
            print("📁 Saved to: data/nse_equity_securities.json")
            print()

            # Show sample data
            print("📋 Sample Securities (first 5):")
            print("-" * 80)
            for i, sec in enumerate(securities[:5], 1):
                print(f"{i}. {sec.get('symbol', 'N/A'):15} | {sec.get('company_name', 'N/A')[:40]:40} | ₹{sec.get('last_price', 0):>10}")

            print()
            print("💡 Tip: Open 'data/nse_equity_securities.json' to see the complete list!")

        else:
            print("⚠️  No securities data retrieved.")
            print("This might be due to NSE website access restrictions.")

    except Exception as e:
        print(f"❌ Error: {e}")

    print()
    print("=" * 80)

    # Method 2: Fetch NIFTY Indices
    print()
    print("📈 Method 2: Fetch All NIFTY Indices")
    print("-" * 80)
    print("Usage: scraper.get_all_nifty_indices()")
    print()
    print("This fetches data for all NIFTY indices (NIFTY 50, NIFTY 500, etc.)")
    print()

    try:
        print("Fetching indices data...")
        indices = scraper.get_all_nifty_indices()

        if indices:
            print(f"✅ Successfully fetched {len(indices)} indices!")
            print()

            # Save to JSON
            scraper.save_to_file(indices, 'nse_nifty_indices.json', 'json')
            print("📁 Saved to: data/nse_nifty_indices.json")
            print()

            # Show sample data
            print("📋 Sample Indices:")
            print("-" * 80)
            for i, idx in enumerate(indices[:10], 1):
                name = idx.get('index_name', 'N/A')
                last = idx.get('last_price', 0)
                change = idx.get('pChange', 0)
                emoji = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
                print(f"{emoji} {name:30} | {last:>10,.2f} | {change:>+6.2f}%")

            print()

        else:
            print("⚠️  No indices data retrieved.")

    except Exception as e:
        print(f"❌ Error: {e}")

    print()
    print("=" * 80)
    print()

    # Usage Examples
    print("🔧 USAGE EXAMPLES")
    print("=" * 80)
    print()

    print("1️⃣  Use in Python Script:")
    print("-" * 80)
    print("""
from nse_scraper import NSEScraper

scraper = NSEScraper()

# Get all securities
securities = scraper.scrape_equity_securities()

# Filter specific stocks
nifty50_symbols = ['HDFCBANK', 'RELIANCE', 'TCS', 'INFY', 'ICICIBANK']
filtered = [s for s in securities if s['symbol'] in nifty50_symbols]

# Get current prices
for stock in filtered:
    print(f"{stock['symbol']}: ₹{stock['last_price']}")
""")

    print()
    print("2️⃣  Use in Streamlit App:")
    print("-" * 80)
    print("""
# The scraper is already integrated in app_enhanced.py
# Navigate to the "📥 Scraper" tab and check "Equity Securities"
# Then click "🚀 Start Scraping"

# Or add your own tab:
import streamlit as st
from nse_scraper import NSEScraper

st.title("NSE Securities Viewer")
scraper = NSEScraper()

if st.button("Fetch Securities"):
    securities = scraper.scrape_equity_securities()
    df = pd.DataFrame(securities)
    st.dataframe(df)
""")

    print()
    print("3️⃣  Export to CSV:")
    print("-" * 80)
    print("""
import pandas as pd

securities = scraper.scrape_equity_securities()
df = pd.DataFrame(securities)
df.to_csv('nse_securities.csv', index=False)

# Now open in Excel or analyze with pandas
""")

    print()
    print("=" * 80)
    print()

    print("📚 AVAILABLE DATA FIELDS")
    print("=" * 80)
    print("""
For each security, you get:

Basic Info:
  - symbol          : Stock symbol (e.g., "HDFCBANK")
  - company_name    : Full company name
  - industry        : Industry/sector classification
  - isin            : ISIN number (unique identifier)

Price Data:
  - last_price      : Current/last traded price
  - change          : Absolute price change
  - pChange         : Percentage change
  - previous_close  : Previous day's closing price
  - open            : Today's opening price
  - close           : Closing price

Range Data:
  - year_high       : 52-week high price
  - year_low        : 52-week low price

Metadata:
  - source          : "NSE"
  - scraped_at      : Timestamp when data was fetched
""")

    print()
    print("=" * 80)
    print("✅ DEMO COMPLETE")
    print("=" * 80)
    print()
    print("💡 Next Steps:")
    print("  1. Run this script: python fetch_nse_securities_demo.py")
    print("  2. Check the 'data' folder for output JSON files")
    print("  3. Open in Streamlit: streamlit run app_enhanced.py")
    print("  4. Integrate into your own scripts!")
    print()


if __name__ == "__main__":
    main()
