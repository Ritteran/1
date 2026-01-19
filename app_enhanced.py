#!/usr/bin/env python3
"""
Enhanced Streamlit Application for NSE/BSE Stock Market Scraper
Full-featured desktop application with data processing and visualization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import sys
from pathlib import Path
from io import BytesIO

# Import scrapers and processor
from nse_scraper import NSEScraper
from bse_scraper import BSEScraper
from data_processor import DataProcessor
from stock_analyzer import StockAnalyzer
import config

# Import NIFTY 50 analyzer modules
sys.path.append(str(Path(__file__).parent / 'nifty50_analyzer' / 'src'))
try:
    from nifty50_analyzer.src.returns_risk import ReturnsRiskCalculator, load_price_data
    from nifty50_analyzer.src.scoring import RatioScorer
    from nifty50_analyzer.src.signal import SignalGenerator
    from nifty50_analyzer.src.reporting import ReportGenerator
    import yaml
    NIFTY50_AVAILABLE = True
except ImportError as e:
    NIFTY50_AVAILABLE = False
    print(f"NIFTY 50 Analyzer not available: {e}")

# Page configuration
st.set_page_config(
    page_title="NSE/BSE Market Data Application",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = {}
if 'loaded_data' not in st.session_state:
    st.session_state.loaded_data = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'nifty50_results' not in st.session_state:
    st.session_state.nifty50_results = None
if 'nifty50_summary' not in st.session_state:
    st.session_state.nifty50_summary = None

# Initialize processor
processor = DataProcessor()


def scraper_tab():
    """Data Scraper Tab"""
    st.header("📥 Data Scraper")
    st.write("Scrape fresh data from NSE and BSE websites")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("⚙️ Scraper Settings")

        # Exchange selection
        exchange = st.radio(
            "Select Exchange:",
            ["Both NSE & BSE", "NSE Only", "BSE Only"]
        )

        # Days
        days = st.slider("Days of data:", 1, 90, 7)

        st.subheader("📋 Data Types")

        # NSE options
        nse_options = {}
        if exchange in ["Both NSE & BSE", "NSE Only"]:
            st.markdown("**NSE:**")
            nse_options['equity_securities'] = st.checkbox("Equity Securities/Instruments", value=False, key="nse_sec")
            nse_options['nifty_indices'] = st.checkbox("NIFTY Indices", value=False, key="nse_idx")
            nse_options['circulars'] = st.checkbox("Circulars", value=True, key="nse_circ")
            nse_options['reports'] = st.checkbox("Daily Reports", value=True, key="nse_rep")
            nse_options['announcements'] = st.checkbox("Announcements", value=False, key="nse_ann")
            nse_options['bhavcopy'] = st.checkbox("Bhavcopy", value=False, key="nse_bhav")

        # BSE options
        bse_options = {}
        if exchange in ["Both NSE & BSE", "BSE Only"]:
            st.markdown("**BSE:**")
            bse_options['circulars'] = st.checkbox("Circulars", value=True, key="bse_circ")
            bse_options['reports'] = st.checkbox("Daily Reports", value=True, key="bse_rep")
            bse_options['actions'] = st.checkbox("Corporate Actions", value=False, key="bse_act")
            bse_options['news'] = st.checkbox("News", value=False, key="bse_news")
            bse_options['bhavcopy'] = st.checkbox("Bhavcopy", value=False, key="bse_bhav")

        scrape_button = st.button("🚀 Start Scraping", type="primary", use_container_width=True)

    with col2:
        st.subheader("📊 Scraping Status")

        if scrape_button:
            has_selection = any(nse_options.values()) or any(bse_options.values())

            if not has_selection:
                st.error("❌ Please select at least one data type!")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()

                all_results = {}

                # NSE scraping
                if exchange in ["Both NSE & BSE", "NSE Only"]:
                    with st.spinner("Scraping NSE data..."):
                        nse_scraper = NSEScraper()

                        if nse_options.get('equity_securities'):
                            status_text.text("📊 Fetching NSE equity securities/instruments...")
                            securities = nse_scraper.scrape_equity_securities()
                            if securities:
                                all_results['NSE_Equity_Securities'] = securities
                                nse_scraper.save_to_file(securities, 'nse_equity_securities.json', 'json')

                        if nse_options.get('nifty_indices'):
                            status_text.text("📈 Fetching NIFTY indices...")
                            indices = nse_scraper.get_all_nifty_indices()
                            if indices:
                                all_results['NSE_NIFTY_Indices'] = indices
                                nse_scraper.save_to_file(indices, 'nse_nifty_indices.json', 'json')

                        if nse_options.get('circulars'):
                            status_text.text("📄 Fetching NSE circulars...")
                            circulars = nse_scraper.scrape_circulars(days=days)
                            if circulars:
                                all_results['NSE_Circulars'] = circulars
                                nse_scraper.save_to_file(circulars, 'nse_circulars.json', 'json')

                        if nse_options.get('reports'):
                            status_text.text("📊 Fetching NSE reports...")
                            reports = nse_scraper.scrape_daily_reports('equity')
                            if reports:
                                all_results['NSE_Reports'] = reports
                                nse_scraper.save_to_file(reports, 'nse_reports.json', 'json')

                        if nse_options.get('announcements'):
                            status_text.text("📢 Fetching NSE announcements...")
                            announcements = nse_scraper.scrape_announcements()
                            if announcements:
                                all_results['NSE_Announcements'] = announcements

                        if nse_options.get('bhavcopy'):
                            status_text.text("📈 Downloading NSE Bhavcopy...")
                            bhavcopy = nse_scraper.scrape_equity_bhavcopy()
                            if bhavcopy:
                                all_results['NSE_Bhavcopy'] = bhavcopy

                    progress_bar.progress(50)

                # BSE scraping
                if exchange in ["Both NSE & BSE", "BSE Only"]:
                    with st.spinner("Scraping BSE data..."):
                        bse_scraper = BSEScraper()

                        if bse_options.get('circulars'):
                            status_text.text("📄 Fetching BSE circulars...")
                            circulars = bse_scraper.scrape_circulars(days=days)
                            if circulars:
                                all_results['BSE_Circulars'] = circulars
                                bse_scraper.save_to_file(circulars, 'bse_circulars.json', 'json')

                        if bse_options.get('reports'):
                            status_text.text("📊 Fetching BSE reports...")
                            reports = bse_scraper.scrape_daily_reports('market_summary')
                            if reports:
                                all_results['BSE_Reports'] = reports

                        if bse_options.get('actions'):
                            status_text.text("🎯 Fetching BSE corporate actions...")
                            actions = bse_scraper.scrape_corporate_actions()
                            if actions:
                                all_results['BSE_Corporate_Actions'] = actions

                        if bse_options.get('news'):
                            status_text.text("📰 Fetching BSE news...")
                            news = bse_scraper.scrape_news()
                            if news:
                                all_results['BSE_News'] = news

                        if bse_options.get('bhavcopy'):
                            status_text.text("📈 Downloading BSE Bhavcopy...")
                            bhavcopy = bse_scraper.scrape_bhavcopy()
                            if bhavcopy:
                                all_results['BSE_Bhavcopy'] = bhavcopy

                progress_bar.progress(100)
                status_text.text("✅ Scraping completed!")

                st.session_state.scraped_data = all_results

                st.success(f"✅ Successfully scraped {len(all_results)} datasets!")

                # Show summary
                for name, data in all_results.items():
                    if isinstance(data, list):
                        st.info(f"**{name}**: {len(data)} records")

        # Display previously scraped data
        if st.session_state.scraped_data:
            st.divider()
            st.subheader("📦 Scraped Datasets")

            for name, data in st.session_state.scraped_data.items():
                with st.expander(f"📁 {name}"):
                    if isinstance(data, list) and len(data) > 0:
                        df = pd.DataFrame(data)
                        st.write(f"**Records:** {len(df)}")
                        st.dataframe(df.head(10), use_container_width=True)

                        # Quick download
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name=f"{name}_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            key=f"download_{name}"
                        )
                    else:
                        st.write(data)


def stock_search_tab():
    """Interactive Stock Search and Analysis Tab"""
    st.header("🔍 Stock Search & Analysis")
    st.write("Search for any stock and get instant analysis with live metrics")

    # Initialize scraper and analyzer
    scraper = NSEScraper()
    analyzer = StockAnalyzer()

    # Search bar
    col_search, col_button = st.columns([4, 1])

    with col_search:
        search_query = st.text_input(
            "Search Symbol or Company Name",
            placeholder="e.g., HDFCBANK, Reliance, TCS...",
            key="stock_search"
        )

    with col_button:
        st.write("")  # Spacer
        st.write("")  # Spacer
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)

    # Quick access buttons for popular stocks
    st.write("**Quick Access:**")
    quick_stocks = ['HDFCBANK', 'RELIANCE', 'TCS', 'INFY', 'ICICIBANK', 'HINDUNILVR', 'ITC', 'SBIN', 'BAJFINANCE', 'BHARTIARTL']

    cols = st.columns(5)
    for i, symbol in enumerate(quick_stocks):
        if cols[i % 5].button(symbol, key=f"quick_{symbol}"):
            search_query = symbol
            search_button = True

    st.divider()

    # Perform search when button clicked or query entered
    if search_button and search_query:
        with st.spinner(f"🔍 Searching for '{search_query}'..."):
            # Get quote data
            quote = scraper.get_symbol_quote(search_query.upper().strip())

            if quote:
                # Perform analysis
                analysis = analyzer.analyze_quote(quote)

                # Display results
                st.success(f"✅ Found: {quote['company_name']}")

                # Basic Info Section
                st.subheader(f"📊 {analysis['basic_info']['symbol']} - {analysis['basic_info']['company_name']}")

                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.write(f"**Industry:** {analysis['basic_info']['industry']}")
                with col_info2:
                    st.write(f"**ISIN:** {analysis['basic_info']['isin']}")

                st.divider()

                # Key Metrics Cards
                st.subheader("💹 Key Metrics")

                price_analysis = analysis['price_analysis']
                valuation = analysis['valuation']
                signals = analysis['signals']

                col1, col2, col3, col4 = st.columns(4)

                # Price card
                with col1:
                    price = price_analysis['last_price']
                    change = price_analysis['pChange']
                    emoji = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
                    st.metric(
                        "Last Price",
                        f"₹{price:,.2f}",
                        f"{change:+.2f}%",
                        delta_color="normal" if change >= 0 else "inverse"
                    )

                # Signal card
                with col2:
                    signal = signals['overall_signal']
                    confidence = signals['confidence_score']
                    signal_color = {
                        'BUY': '🟢',
                        'ACCUMULATE': '🔵',
                        'HOLD': '⚪',
                        'REDUCE': '🟠',
                        'SELL': '🔴'
                    }.get(signal, '⚪')
                    st.metric(
                        "Signal",
                        f"{signal_color} {signal}",
                        f"Confidence: {confidence}"
                    )

                # Volume card
                with col3:
                    volume_data = analysis['volume_analysis']
                    volume_cr = volume_data['volume'] / 10000000  # Convert to Cr
                    st.metric(
                        "Volume",
                        f"{volume_cr:.2f} Cr",
                        f"Delivery: {volume_data['delivery_percentage']:.1f}%"
                    )

                # Market Cap card
                with col4:
                    mcap = valuation['market_cap']
                    mcap_cr = mcap / 100 if mcap > 0 else 0
                    st.metric(
                        "Market Cap",
                        f"₹{mcap_cr:,.0f} Cr",
                        valuation['market_cap_category']
                    )

                st.divider()

                # Price Analysis Section
                col_left, col_right = st.columns([1, 1])

                with col_left:
                    st.subheader("📈 Price Analysis")

                    # Day range
                    day_range_pct = price_analysis['day_range_pct']
                    st.write("**Today's Range:**")
                    st.progress(day_range_pct / 100)
                    st.write(f"Position: {day_range_pct:.1f}% of day's range")

                    # 52-week range
                    week_52_pct = price_analysis['week_52_range_pct']
                    st.write("**52-Week Range:**")
                    st.progress(week_52_pct / 100)
                    st.write(f"Position: {week_52_pct:.1f}% of 52-week range")

                    # Distances
                    st.write(f"**Distance from 52W High:** {price_analysis['distance_from_52w_high']:.2f}%")
                    st.write(f"**Distance from 52W Low:** {price_analysis['distance_from_52w_low']:.2f}%")
                    st.write(f"**Intraday Gain:** {price_analysis['intraday_gain']:.2f}%")

                with col_right:
                    st.subheader("💡 Signals & Insights")

                    # Overall signal with explanation
                    signal_emoji = {
                        'BUY': '🟢',
                        'ACCUMULATE': '🔵',
                        'HOLD': '⚪',
                        'REDUCE': '🟠',
                        'SELL': '🔴'
                    }.get(signals['overall_signal'], '⚪')

                    st.markdown(f"### {signal_emoji} {signals['overall_signal']}")
                    st.write(f"**Confidence Score:** {signals['confidence_score']}")

                    # Individual signals
                    if signals['signals']:
                        st.write("**Key Indicators:**")
                        for signal in signals['signals']:
                            st.write(f"• {signal}")
                    else:
                        st.info("No significant signals detected")

                st.divider()

                # Valuation & Technical Section
                col_val, col_tech = st.columns([1, 1])

                with col_val:
                    st.subheader("💰 Valuation Metrics")

                    val_data = [
                        ("P/E Ratio", f"{valuation['pe_ratio']:.2f}" if valuation['pe_ratio'] > 0 else "N/A"),
                        ("P/B Ratio", f"{valuation['pb_ratio']:.2f}" if valuation['pb_ratio'] > 0 else "N/A"),
                        ("Dividend Yield", f"{valuation['dividend_yield']:.2f}%" if valuation['dividend_yield'] > 0 else "N/A"),
                        ("Book Value", f"₹{valuation['book_value']:.2f}" if valuation['book_value'] > 0 else "N/A"),
                        ("Face Value", f"₹{valuation['face_value']:.2f}" if valuation['face_value'] > 0 else "N/A"),
                    ]

                    for label, value in val_data:
                        col_a, col_b = st.columns([2, 1])
                        col_a.write(f"**{label}:**")
                        col_b.write(value)

                    # Valuation assessment
                    assessment = valuation['valuation_assessment']
                    assessment_color = {
                        'Undervalued': '🟢',
                        'Fairly Valued': '🟡',
                        'Overvalued': '🟠',
                        'Highly Overvalued': '🔴',
                        'Unknown': '⚪'
                    }.get(assessment, '⚪')
                    st.info(f"{assessment_color} Assessment: **{assessment}**")

                with col_tech:
                    st.subheader("📊 Technical Indicators")

                    tech = analysis['technical_indicators']

                    tech_data = [
                        ("Price Momentum", f"{tech['price_momentum']:+.2f}%"),
                        ("Support Level", f"₹{tech['support_level']:.2f}"),
                        ("Resistance Level", f"₹{tech['resistance_level']:.2f}"),
                        ("Pivot Point", f"₹{tech['pivot_point']:.2f}"),
                        ("From Support", f"{tech['distance_from_support']:.2f}%"),
                        ("To Resistance", f"{tech['distance_from_resistance']:.2f}%"),
                    ]

                    for label, value in tech_data:
                        col_a, col_b = st.columns([2, 1])
                        col_a.write(f"**{label}:**")
                        col_b.write(value)

                st.divider()

                # Risk Analysis Section
                st.subheader("⚠️ Risk Analysis")

                risk = analysis['risk_metrics']

                col_risk1, col_risk2, col_risk3 = st.columns(3)

                with col_risk1:
                    risk_color = {
                        'Low': '🟢',
                        'Moderate': '🟡',
                        'High': '🟠',
                        'Very High': '🔴'
                    }.get(risk['risk_level'], '⚪')
                    st.metric("Risk Level", f"{risk_color} {risk['risk_level']}")

                with col_risk2:
                    st.metric("Intraday Volatility", f"{risk['intraday_volatility']:.2f}%")

                with col_risk3:
                    if risk['circuit_warnings']:
                        for warning in risk['circuit_warnings']:
                            st.warning(warning)
                    else:
                        st.success("✅ No circuit warnings")

                # Volume Analysis
                st.divider()
                st.subheader("📊 Volume & Delivery Analysis")

                vol = analysis['volume_analysis']

                col_vol1, col_vol2, col_vol3 = st.columns(3)

                with col_vol1:
                    st.metric("Total Volume", f"{vol['volume']/10000000:.2f} Cr")

                with col_vol2:
                    st.metric("Traded Value", f"₹{vol['value']/10000000:.0f} Cr")

                with col_vol3:
                    delivery_emoji = "💪" if vol['delivery_strength'] == 'Strong' else "📊" if vol['delivery_strength'] == 'Moderate' else "⚠️"
                    st.metric("Delivery Strength", f"{delivery_emoji} {vol['delivery_strength']}")

                # Export data
                st.divider()
                st.subheader("💾 Export Data")

                # Prepare export data
                export_data = {
                    'Symbol': analysis['basic_info']['symbol'],
                    'Company': analysis['basic_info']['company_name'],
                    'Industry': analysis['basic_info']['industry'],
                    'Last Price': price_analysis['last_price'],
                    'Change %': price_analysis['pChange'],
                    'Signal': signals['overall_signal'],
                    'Confidence': signals['confidence_score'],
                    'P/E Ratio': valuation['pe_ratio'],
                    'Market Cap (Cr)': valuation['market_cap'] / 100,
                    'Volume (Cr)': vol['volume'] / 10000000,
                    'Delivery %': vol['delivery_percentage'],
                    'Risk Level': risk['risk_level'],
                    'Valuation': valuation['valuation_assessment']
                }

                df_export = pd.DataFrame([export_data])
                csv = df_export.to_csv(index=False)

                col_exp1, col_exp2 = st.columns(2)

                with col_exp1:
                    st.download_button(
                        label="📥 Download Analysis (CSV)",
                        data=csv,
                        file_name=f"{analysis['basic_info']['symbol']}_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )

                with col_exp2:
                    # Create summary text
                    summary_text = f"""
Stock Analysis Summary - {analysis['basic_info']['symbol']}
Company: {analysis['basic_info']['company_name']}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Price Information:
- Last Price: ₹{price_analysis['last_price']:.2f}
- Change: {price_analysis['pChange']:+.2f}%
- Day Range: {price_analysis['day_range_pct']:.1f}%

Trading Signal: {signals['overall_signal']} (Confidence: {signals['confidence_score']})

Key Indicators:
{chr(10).join('- ' + s for s in signals['signals'])}

Valuation:
- P/E Ratio: {valuation['pe_ratio']:.2f}
- Assessment: {valuation['valuation_assessment']}
- Market Cap: ₹{valuation['market_cap']/100:.0f} Cr

Risk Level: {risk['risk_level']}
Delivery %: {vol['delivery_percentage']:.1f}%

---
Generated by NSE/BSE Market Data Application
                    """

                    st.download_button(
                        label="📥 Download Summary (TXT)",
                        data=summary_text,
                        file_name=f"{analysis['basic_info']['symbol']}_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )

            else:
                st.error(f"❌ Could not find data for '{search_query}'")
                st.info("💡 Try searching by exact symbol (e.g., HDFCBANK, RELIANCE, TCS)")

                # Suggest similar symbols
                with st.spinner("Searching for similar symbols..."):
                    matches = scraper.search_symbols(search_query)
                    if matches:
                        st.write("**Did you mean:**")
                        for match in matches[:5]:
                            if st.button(f"{match['symbol']} - {match.get('company_name', 'N/A')}", key=f"suggest_{match['symbol']}"):
                                st.rerun()

    elif not search_query:
        # Show welcome message and instructions
        st.info("👆 Enter a stock symbol or company name above to get started")

        st.write("### 🚀 How to Use:")
        st.write("1. **Type a symbol** (e.g., HDFCBANK) or company name in the search box")
        st.write("2. **Click Search** or press Enter")
        st.write("3. **View comprehensive analysis** with live metrics and signals")
        st.write("4. **Export data** to CSV or text file for further analysis")

        st.write("### 📊 What You Get:")
        col_feat1, col_feat2 = st.columns(2)

        with col_feat1:
            st.write("**Price Analysis:**")
            st.write("• Real-time price and changes")
            st.write("• Day and 52-week ranges")
            st.write("• Support/Resistance levels")

            st.write("**Trading Signals:**")
            st.write("• Buy/Sell/Hold recommendations")
            st.write("• Confidence scores")
            st.write("• Key indicators")

        with col_feat2:
            st.write("**Valuation Metrics:**")
            st.write("• P/E and P/B ratios")
            st.write("• Market cap category")
            st.write("• Dividend yield")

            st.write("**Risk Analysis:**")
            st.write("• Volatility assessment")
            st.write("• Delivery percentage")
            st.write("• Circuit warnings")


def data_loader_tab():
    """Data Loader Tab"""
    st.header("📂 Data Loader")
    st.write("Load and view previously scraped data")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📁 Available Files")

        # List files in data directory
        data_files = list(config.DATA_DIR.glob('*.json')) + \
                    list(config.DATA_DIR.glob('*.csv')) + \
                    list(config.DATA_DIR.glob('*.xlsx'))

        if not data_files:
            st.warning("No data files found in the data directory.")
            st.info("💡 Tip: Scrape some data first using the Scraper tab!")
        else:
            file_options = [f.name for f in data_files]
            selected_file = st.selectbox("Select a file:", file_options)

            if st.button("📖 Load File", type="primary"):
                file_path = config.DATA_DIR / selected_file
                try:
                    df = processor.load_data(str(file_path))
                    st.session_state.loaded_data = df
                    st.success(f"✅ Loaded {len(df)} records from {selected_file}")
                except Exception as e:
                    st.error(f"❌ Error loading file: {e}")

            # Upload file
            st.divider()
            st.subheader("📤 Upload File")
            uploaded_file = st.file_uploader(
                "Upload your own data file",
                type=['json', 'csv', 'xlsx']
            )

            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('.json'):
                        data = json.load(uploaded_file)
                        df = pd.DataFrame(data if isinstance(data, list) else [data])
                    elif uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(uploaded_file)

                    st.session_state.loaded_data = df
                    st.success(f"✅ Loaded {len(df)} records from uploaded file")
                except Exception as e:
                    st.error(f"❌ Error loading uploaded file: {e}")

    with col2:
        if st.session_state.loaded_data is not None:
            df = st.session_state.loaded_data

            st.subheader("📊 Data Overview")

            # Summary stats
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Total Records", len(df))
            col_b.metric("Columns", len(df.columns))
            col_c.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

            # Data preview
            st.subheader("👀 Data Preview")
            st.dataframe(df.head(20), use_container_width=True)

            # Column info
            with st.expander("ℹ️ Column Information"):
                col_info = pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes.values,
                    'Non-Null Count': df.count().values,
                    'Null Count': df.isnull().sum().values
                })
                st.dataframe(col_info, use_container_width=True)

            # Quick stats
            with st.expander("📈 Quick Statistics"):
                stats = processor.get_summary_stats(df)
                st.json(stats)
        else:
            st.info("👈 Load a data file from the sidebar to view it here")


def data_processor_tab():
    """Data Processor Tab"""
    st.header("⚙️ Data Processor")
    st.write("Filter, search, and transform your data")

    if st.session_state.loaded_data is None:
        st.warning("⚠️ No data loaded. Please load data from the Data Loader tab first.")
        return

    df = st.session_state.loaded_data.copy()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🔧 Processing Options")

        # Clean data
        if st.checkbox("🧹 Clean Data", value=True):
            df = processor.clean_data(df)
            st.success("✅ Data cleaned (removed duplicates, standardized formats)")

        # Date filter
        st.divider()
        st.subheader("📅 Date Filter")

        date_columns = [col for col in df.columns if 'date' in col.lower()]
        if date_columns:
            date_col = st.selectbox("Date column:", date_columns)

            use_date_filter = st.checkbox("Enable date filtering")
            if use_date_filter:
                col_a, col_b = st.columns(2)
                start_date = col_a.date_input("Start date", datetime.now() - timedelta(days=30))
                end_date = col_b.date_input("End date", datetime.now())

                df = processor.filter_by_date(
                    df, date_col,
                    start_date.strftime('%Y-%m-%d'),
                    end_date.strftime('%Y-%m-%d')
                )

        # Keyword filter
        st.divider()
        st.subheader("🔍 Keyword Filter")

        text_columns = df.select_dtypes(include=['object']).columns.tolist()
        if text_columns:
            search_col = st.selectbox("Search in column:", ['All columns'] + text_columns)
            keywords = st.text_input("Keywords (comma-separated):", "")

            if keywords:
                keyword_list = [k.strip() for k in keywords.split(',')]
                if search_col == 'All columns':
                    df = processor.search_data(df, keywords, text_columns)
                else:
                    df = processor.filter_by_keywords(df, search_col, keyword_list)

        # Company filter
        st.divider()
        st.subheader("🏢 Company Filter")

        company_columns = [col for col in df.columns if any(x in col.lower() for x in ['company', 'symbol'])]
        if company_columns:
            companies_input = st.text_input("Companies (comma-separated):", "")
            if companies_input:
                company_list = [c.strip() for c in companies_input.split(',')]
                df = processor.filter_by_company(df, company_list)

        # Apply filters
        if st.button("✨ Apply Filters", type="primary"):
            st.session_state.processed_data = df
            st.success(f"✅ Processed! {len(df)} records remaining")

    with col2:
        st.subheader("📊 Processed Data")

        if st.session_state.processed_data is not None:
            processed_df = st.session_state.processed_data
        else:
            processed_df = df

        # Show metrics
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Original Records", len(st.session_state.loaded_data))
        col_b.metric("Filtered Records", len(processed_df))
        col_c.metric("Removed", len(st.session_state.loaded_data) - len(processed_df))

        # Show data
        st.dataframe(processed_df, use_container_width=True)

        # Export options
        st.divider()
        st.subheader("💾 Export Processed Data")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            csv = processed_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        with col_b:
            json_str = processed_df.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

        with col_c:
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                processed_df.to_excel(writer, index=False, sheet_name='Processed Data')
            st.download_button(
                label="📥 Download Excel",
                data=buffer.getvalue(),
                file_name=f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


def visualization_tab():
    """Data Visualization Tab"""
    st.header("📊 Data Visualization")
    st.write("Visualize trends and patterns in your data")

    if st.session_state.loaded_data is None:
        st.warning("⚠️ No data loaded. Please load data from the Data Loader tab first.")
        return

    df = st.session_state.processed_data if st.session_state.processed_data is not None else st.session_state.loaded_data

    # Chart type selection
    chart_type = st.selectbox(
        "Select Chart Type:",
        ["📈 Time Series", "📊 Bar Chart", "🥧 Pie Chart", "📉 Trend Analysis", "🔥 Heatmap"]
    )

    if chart_type == "📈 Time Series":
        st.subheader("Time Series Analysis")

        date_columns = [col for col in df.columns if 'date' in col.lower()]
        if not date_columns:
            st.warning("No date columns found in the data.")
            return

        date_col = st.selectbox("Date column:", date_columns)
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col])

        # Group by date and count
        time_series = df.groupby(df[date_col].dt.date).size().reset_index()
        time_series.columns = ['Date', 'Count']

        fig = px.line(time_series, x='Date', y='Count',
                     title='Activity Over Time',
                     labels={'Count': 'Number of Records'})
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Show statistics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Days", len(time_series))
        col2.metric("Avg per Day", f"{time_series['Count'].mean():.1f}")
        col3.metric("Peak Day", f"{time_series['Count'].max()}")

    elif chart_type == "📊 Bar Chart":
        st.subheader("Bar Chart Analysis")

        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        if not categorical_cols:
            st.warning("No categorical columns found.")
            return

        cat_col = st.selectbox("Category column:", categorical_cols)

        # Count by category
        counts = df[cat_col].value_counts().head(15)

        fig = px.bar(x=counts.index, y=counts.values,
                    title=f'Distribution of {cat_col}',
                    labels={'x': cat_col, 'y': 'Count'})
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "🥧 Pie Chart":
        st.subheader("Pie Chart Analysis")

        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        if not categorical_cols:
            st.warning("No categorical columns found.")
            return

        cat_col = st.selectbox("Category column:", categorical_cols)
        top_n = st.slider("Show top N categories:", 5, 20, 10)

        # Count by category
        counts = df[cat_col].value_counts().head(top_n)

        fig = px.pie(values=counts.values, names=counts.index,
                    title=f'Distribution of {cat_col}')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "📉 Trend Analysis":
        st.subheader("Trend Analysis")

        date_columns = [col for col in df.columns if 'date' in col.lower()]
        if not date_columns:
            st.warning("No date columns found.")
            return

        date_col = st.selectbox("Date column:", date_columns)

        trends = processor.detect_trends(df, date_col)

        st.write("### Overall Trend")
        if trends['overall_trend'] == 'increasing':
            st.success("📈 Activity is INCREASING over time")
        elif trends['overall_trend'] == 'decreasing':
            st.warning("📉 Activity is DECREASING over time")
        else:
            st.info("➡️ Activity is STABLE")

        col1, col2 = st.columns(2)

        with col1:
            st.write("### 🔥 Peak Days")
            if trends['peak_days']:
                peak_df = pd.DataFrame(list(trends['peak_days'].items()),
                                      columns=['Date', 'Records'])
                st.dataframe(peak_df, use_container_width=True)

        with col2:
            st.write("### 🔻 Quiet Days")
            if trends['quiet_days']:
                quiet_df = pd.DataFrame(list(trends['quiet_days'].items()),
                                       columns=['Date', 'Records'])
                st.dataframe(quiet_df, use_container_width=True)

    elif chart_type == "🔥 Heatmap":
        st.subheader("Activity Heatmap")

        date_columns = [col for col in df.columns if 'date' in col.lower()]
        if not date_columns:
            st.warning("No date columns found.")
            return

        date_col = st.selectbox("Date column:", date_columns)
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col])

        # Create heatmap data
        df['weekday'] = df[date_col].dt.day_name()
        df['week'] = df[date_col].dt.isocalendar().week

        heatmap_data = df.groupby(['week', 'weekday']).size().reset_index(name='count')
        heatmap_pivot = heatmap_data.pivot(index='weekday', columns='week', values='count')

        # Order weekdays
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_pivot = heatmap_pivot.reindex(weekday_order)

        fig = px.imshow(heatmap_pivot,
                       labels=dict(x="Week Number", y="Day of Week", color="Records"),
                       title="Activity Heatmap by Week and Day",
                       aspect="auto")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)


def analytics_tab():
    """Analytics Tab"""
    st.header("📈 Advanced Analytics")
    st.write("Deep insights and comparisons")

    if st.session_state.loaded_data is None:
        st.warning("⚠️ No data loaded. Please load data from the Data Loader tab first.")
        return

    df = st.session_state.processed_data if st.session_state.processed_data is not None else st.session_state.loaded_data

    # Summary Statistics
    st.subheader("📊 Summary Statistics")

    stats = processor.get_summary_stats(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", stats['total_records'])
    col2.metric("Columns", len(stats['columns']))
    col3.metric("Unique Companies", stats.get('company_count', 'N/A'))

    if stats['date_range'].get('start'):
        col4.metric("Date Range",
                   f"{stats['date_range']['start']} to {stats['date_range']['end']}")

    # Category breakdown
    if stats['category_breakdown']:
        st.subheader("📋 Category Breakdown")

        cat_df = pd.DataFrame(list(stats['category_breakdown'].items()),
                             columns=['Category', 'Count'])
        cat_df = cat_df.sort_values('Count', ascending=False)

        fig = px.bar(cat_df, x='Category', y='Count',
                    title='Top Categories by Count')
        st.plotly_chart(fig, use_container_width=True)

    # Data quality
    st.subheader("✅ Data Quality")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Missing Values")
        missing = df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)

        if len(missing) > 0:
            missing_df = pd.DataFrame({
                'Column': missing.index,
                'Missing Count': missing.values,
                'Percentage': (missing.values / len(df) * 100).round(2)
            })
            st.dataframe(missing_df, use_container_width=True)
        else:
            st.success("✅ No missing values found!")

    with col2:
        st.write("### Duplicate Records")
        duplicates = df.duplicated().sum()
        st.metric("Duplicate Rows", duplicates)

        if duplicates > 0:
            st.warning(f"⚠️ Found {duplicates} duplicate records")
            if st.button("Remove Duplicates"):
                df = df.drop_duplicates()
                st.session_state.processed_data = df
                st.success("✅ Duplicates removed!")
        else:
            st.success("✅ No duplicates found!")

    # Advanced filters
    st.divider()
    st.subheader("🔍 Advanced Search")

    search_term = st.text_input("Search across all columns:", "")
    if search_term:
        result = processor.search_data(df, search_term)
        st.write(f"**Found {len(result)} matching records:**")
        st.dataframe(result, use_container_width=True)


def nifty50_analyzer_tab():
    """NIFTY 50 Stock Analyzer Tab"""
    st.header("🎯 NIFTY 50 Stock Analyzer")
    st.write("Analyze all 50 NIFTY stocks with sector-specific benchmarks and risk-adjusted returns")

    if not NIFTY50_AVAILABLE:
        st.error("❌ NIFTY 50 Analyzer modules not available. Please check installation.")
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📁 Data Input")

        # File upload option
        input_method = st.radio(
            "Input Method:",
            ["📤 Upload Files", "📂 Use Template Files"]
        )

        if input_method == "📤 Upload Files":
            st.write("**Upload your data files:**")

            price_file = st.file_uploader(
                "1. Price Data (CSV with 1 year daily prices)",
                type=['csv'],
                key='price_upload'
            )

            fundamentals_file = st.file_uploader(
                "2. Fundamentals Data (CSV with financial ratios)",
                type=['csv'],
                key='fundamentals_upload'
            )

            # Sector mapping is provided
            st.info("💡 Sector mapping is pre-configured (no upload needed)")

        else:
            st.info("📋 Using template files from nifty50_analyzer/inputs/")
            st.write("Make sure you've filled in:")
            st.write("- ✅ prices.csv")
            st.write("- ✅ fundamentals.csv")
            price_file = None
            fundamentals_file = None

        st.divider()
        st.subheader("⚙️ Configuration")

        # Risk-free rate
        risk_free_rate = st.number_input(
            "Risk-Free Rate (%):",
            min_value=0.0,
            max_value=20.0,
            value=6.5,
            step=0.5,
            help="Usually government bond yield (10Y)"
        ) / 100

        # Signal thresholds
        st.write("**Signal Thresholds:**")
        buy_threshold = st.slider(
            "BUY Threshold (Percentile):",
            60, 95, 80,
            help="Top X% = BUY signal"
        )
        avoid_threshold = st.slider(
            "AVOID Threshold (Percentile):",
            5, 40, 20,
            help="Bottom X% = AVOID signal"
        )

        # Composite weights
        st.write("**Composite Score Weights:**")
        weight_financial = st.slider("Financial Strength:", 0, 100, 40, 5) / 100
        weight_growth = st.slider("Growth & Efficiency:", 0, 100, 30, 5) / 100
        weight_risk = st.slider("Risk-Adjusted Return:", 0, 100, 30, 5) / 100

        # Normalize weights
        total_weight = weight_financial + weight_growth + weight_risk
        if total_weight != 1.0:
            st.warning(f"⚠️ Weights sum to {total_weight*100:.0f}% (will be normalized to 100%)")
            weight_financial /= total_weight
            weight_growth /= total_weight
            weight_risk /= total_weight

        st.divider()

        # Run analysis button
        run_analysis = st.button(
            "🚀 Run Analysis",
            type="primary",
            use_container_width=True
        )

    with col2:
        st.subheader("📊 Analysis Results")

        if run_analysis:
            try:
                # Load configuration
                config_path = Path(__file__).parent / 'nifty50_analyzer' / 'config.yml'
                benchmarks_path = Path(__file__).parent / 'nifty50_analyzer' / 'sector_benchmarks.yml'

                with open(config_path, 'r') as f:
                    config_data = yaml.safe_load(f)

                with open(benchmarks_path, 'r') as f:
                    benchmarks = yaml.safe_load(f)

                # Update config with user settings
                config_data['risk_free_rate'] = risk_free_rate
                config_data['signals']['buy_threshold'] = buy_threshold
                config_data['signals']['avoid_threshold'] = avoid_threshold
                config_data['weights']['financial_strength'] = weight_financial
                config_data['weights']['growth_efficiency'] = weight_growth
                config_data['weights']['risk_adjusted_return'] = weight_risk

                # Load data
                with st.spinner("📂 Loading data..."):
                    if input_method == "📤 Upload Files":
                        if not price_file or not fundamentals_file:
                            st.error("❌ Please upload both price and fundamentals files")
                            return

                        prices_df = pd.read_csv(price_file, index_col=0, parse_dates=True)
                        fundamentals_df = pd.read_csv(fundamentals_file)
                    else:
                        inputs_dir = Path(__file__).parent / 'nifty50_analyzer' / 'inputs'
                        prices_df = pd.read_csv(inputs_dir / 'prices.csv', index_col=0, parse_dates=True)
                        fundamentals_df = pd.read_csv(inputs_dir / 'fundamentals.csv')

                    sector_mapping_df = pd.read_csv(
                        Path(__file__).parent / 'nifty50_analyzer' / 'inputs' / 'sector_mapping.csv'
                    )

                # Initialize modules
                with st.spinner("🔧 Initializing analyzer..."):
                    returns_calculator = ReturnsRiskCalculator(trading_days=252)
                    scorer = RatioScorer(benchmarks=benchmarks, weights=config_data['weights'])
                    signal_generator = SignalGenerator(config=config_data['signals'])

                # Calculate returns and risk
                with st.spinner("📈 Calculating returns & volatility..."):
                    returns_df = returns_calculator.analyze_portfolio(prices_df, risk_free_rate=risk_free_rate)

                # Score fundamentals
                with st.spinner("🎯 Scoring fundamentals..."):
                    fundamentals_with_sector = fundamentals_df.merge(
                        sector_mapping_df[['Company', 'Sector']],
                        on='Company',
                        how='left'
                    )
                    scores_df = scorer.score_portfolio(fundamentals_with_sector)

                # Combine analysis
                with st.spinner("🔄 Combining analysis..."):
                    returns_df_reset = returns_df.reset_index().rename(columns={'index': 'symbol'})
                    combined = scores_df.merge(returns_df_reset, left_on='symbol', right_on='symbol', how='inner')

                    # Add sector if not present
                    if 'sector' not in combined.columns:
                        sector_map = sector_mapping_df.set_index('Company')['Sector'].to_dict()
                        combined['sector'] = combined['symbol'].map(sector_map)

                # Generate signals
                with st.spinner("🚦 Generating signals..."):
                    signals_df, summary = signal_generator.generate_portfolio_signals(combined)
                    summary = signal_generator.generate_summary_stats(signals_df)

                # Store results
                st.session_state.nifty50_results = signals_df
                st.session_state.nifty50_summary = summary

                st.success("✅ Analysis complete!")

            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")
                import traceback
                with st.expander("Show error details"):
                    st.code(traceback.format_exc())
                return

        # Display results if available
        if st.session_state.nifty50_results is not None:
            signals_df = st.session_state.nifty50_results
            summary = st.session_state.nifty50_summary

            # Summary statistics
            st.subheader("📈 Executive Summary")

            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("🟢 BUY", summary.get('buy_count', 0))
            col_b.metric("🟡 HOLD", summary.get('hold_count', 0))
            col_c.metric("🔴 AVOID", summary.get('avoid_count', 0))
            col_d.metric("⭐ High Conviction", summary.get('high_confidence_buys', 0))

            # Top BUY picks
            st.divider()
            st.subheader("⭐ Top BUY Picks")

            buys = signals_df[signals_df['signal'] == 'BUY'].sort_values('composite_score', ascending=False).head(10)

            if len(buys) > 0:
                for idx, row in buys.iterrows():
                    with st.expander(f"🟢 **{row.get('symbol', idx)}** - {row.get('sector', 'N/A')} (Score: {row.get('composite_score', 0):.1f})"):
                        col_x, col_y = st.columns(2)

                        with col_x:
                            st.write("**Metrics:**")
                            st.write(f"- Expected Return: {row.get('expected_return_pct', 0):.1f}%")
                            st.write(f"- Volatility: {row.get('volatility_pct', 0):.1f}%")
                            st.write(f"- Sharpe Ratio: {row.get('sharpe_ratio', 0):.2f}")

                        with col_y:
                            st.write("**Scores:**")
                            st.write(f"- Composite: {row.get('composite_score', 0):.1f}")
                            st.write(f"- Percentile: {row.get('percentile', 0):.0f}%")
                            st.write(f"- Confidence: {row.get('confidence', 'N/A')}")

                        st.info(f"💡 {row.get('explanation', 'No explanation available')}")
            else:
                st.warning("No BUY signals generated")

            # Complete results table
            st.divider()
            st.subheader("📋 Complete Results")

            # Color-coded display
            def color_signal(val):
                if val == 'BUY':
                    return 'background-color: #d4edda; color: #155724'
                elif val == 'AVOID':
                    return 'background-color: #f8d7da; color: #721c24'
                else:
                    return 'background-color: #fff3cd; color: #856404'

            # Select display columns
            display_cols = ['symbol', 'sector', 'signal', 'confidence', 'composite_score',
                          'percentile', 'risk_count', 'expected_return_pct', 'volatility_pct']
            display_cols = [col for col in display_cols if col in signals_df.columns]

            styled_df = signals_df[display_cols].style.applymap(
                color_signal,
                subset=['signal']
            ).format({
                'composite_score': '{:.1f}',
                'percentile': '{:.0f}%',
                'expected_return_pct': '{:.1f}%',
                'volatility_pct': '{:.1f}%'
            })

            st.dataframe(styled_df, use_container_width=True)

            # Download options
            st.divider()
            st.subheader("💾 Download Reports")

            col_x, col_y, col_z = st.columns(3)

            with col_x:
                # Summary CSV
                summary_df = signals_df[display_cols].copy()
                csv = summary_df.to_csv(index=False)
                st.download_button(
                    label="📥 Summary CSV",
                    data=csv,
                    file_name=f"nifty50_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

            with col_y:
                # Detailed CSV
                csv_detailed = signals_df.to_csv(index=False)
                st.download_button(
                    label="📥 Detailed CSV",
                    data=csv_detailed,
                    file_name=f"nifty50_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

            with col_z:
                # Generate HTML report
                try:
                    reporter = ReportGenerator(output_dir='.')
                    html_content = reporter._build_html_structure(signals_df, summary, config_data)

                    st.download_button(
                        label="📥 HTML Report",
                        data=html_content,
                        file_name=f"nifty50_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html"
                    )
                except:
                    st.warning("HTML report generation unavailable")

        else:
            st.info("👈 Configure settings and click 'Run Analysis' to get started!")

            # Show sample template
            st.write("### 📋 Sample Data Format")

            with st.expander("Price Data Format"):
                st.write("**prices.csv** should have:")
                st.code("""Date,HDFCBANK,RELIANCE,TCS,...
2024-01-01,1650.50,2450.75,3890.20,...
2024-01-02,1652.30,2455.10,3895.50,...
...
(252 trading days total)""", language="csv")

            with st.expander("Fundamentals Data Format"):
                st.write("**fundamentals.csv** should have:")
                st.code("""Company,ROE,Debt_to_Equity,EBITDA_Margin,...
HDFCBANK,15.2,0.85,45.3,...
RELIANCE,12.5,0.65,25.8,...
...""", language="csv")


def main():
    """Main application"""

    # Header
    st.markdown('<h1 class="main-header">📈 NSE/BSE Market Data Application</h1>',
                unsafe_allow_html=True)

    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📥 Scraper",
        "🔍 Stock Search",
        "📂 Data Loader",
        "⚙️ Processor",
        "📊 Visualization",
        "📈 Analytics",
        "🎯 NIFTY 50 Analyzer"
    ])

    with tab1:
        scraper_tab()

    with tab2:
        stock_search_tab()

    with tab3:
        data_loader_tab()

    with tab4:
        data_processor_tab()

    with tab5:
        visualization_tab()

    with tab6:
        analytics_tab()

    with tab7:
        nifty50_analyzer_tab()

    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
    <p><b>NSE/BSE Market Data Application</b> | Made with ❤️ using Streamlit</p>
    <p><small>Always verify critical data with official sources</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
