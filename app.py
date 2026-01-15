#!/usr/bin/env python3
"""
Streamlit GUI for NSE/BSE Webscraper
User-friendly interface for non-technical users
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from pathlib import Path
import time

# Import scrapers
from nse_scraper import NSEScraper
from bse_scraper import BSEScraper
import config

# Page configuration
st.set_page_config(
    page_title="NSE/BSE Webscraper",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = {}
if 'scraping_status' not in st.session_state:
    st.session_state.scraping_status = {}


def display_header():
    """Display the main header"""
    st.markdown('<h1 class="main-header">📈 NSE/BSE Stock Market Scraper</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    <b>Welcome!</b> This tool helps you extract circulars, reports, and announcements from
    NSE (National Stock Exchange) and BSE (Bombay Stock Exchange) websites.
    <br><br>
    <b>How to use:</b> Simply select what you want to scrape, click the "Start Scraping" button,
    and download your data!
    </div>
    """, unsafe_allow_html=True)


def sidebar_settings():
    """Create sidebar with settings"""
    st.sidebar.header("⚙️ Settings")

    # Exchange selection
    st.sidebar.subheader("1️⃣ Select Exchange")
    exchange = st.sidebar.radio(
        "Choose which stock exchange to scrape:",
        ["Both NSE & BSE", "NSE Only", "BSE Only"],
        help="NSE = National Stock Exchange, BSE = Bombay Stock Exchange"
    )

    # Data selection
    st.sidebar.subheader("2️⃣ Select Data Types")

    # NSE options
    if exchange in ["Both NSE & BSE", "NSE Only"]:
        st.sidebar.markdown("**NSE Data:**")
        nse_circulars = st.sidebar.checkbox("📄 Circulars & Announcements", value=True, key="nse_circulars")
        nse_reports = st.sidebar.checkbox("📊 Daily Market Reports", value=True, key="nse_reports")
        nse_announcements = st.sidebar.checkbox("📢 Latest Announcements", value=False, key="nse_announcements")
        nse_bhavcopy = st.sidebar.checkbox("📈 Bhavcopy (Daily Report)", value=False, key="nse_bhavcopy")
    else:
        nse_circulars = nse_reports = nse_announcements = nse_bhavcopy = False

    # BSE options
    if exchange in ["Both NSE & BSE", "BSE Only"]:
        st.sidebar.markdown("**BSE Data:**")
        bse_circulars = st.sidebar.checkbox("📄 Circulars & Announcements", value=True, key="bse_circulars")
        bse_reports = st.sidebar.checkbox("📊 Daily Market Reports", value=True, key="bse_reports")
        bse_actions = st.sidebar.checkbox("🎯 Corporate Actions", value=False, key="bse_actions")
        bse_news = st.sidebar.checkbox("📰 News Updates", value=False, key="bse_news")
        bse_bhavcopy = st.sidebar.checkbox("📈 Bhavcopy (Daily Report)", value=False, key="bse_bhavcopy")
    else:
        bse_circulars = bse_reports = bse_actions = bse_news = bse_bhavcopy = False

    # Time range
    st.sidebar.subheader("3️⃣ Time Range")
    days = st.sidebar.slider(
        "Number of days to fetch:",
        min_value=1,
        max_value=90,
        value=7,
        help="How many days of historical data to fetch"
    )

    # Advanced options
    with st.sidebar.expander("🔧 Advanced Options"):
        output_format = st.multiselect(
            "Output formats:",
            ["JSON", "CSV", "Excel"],
            default=["JSON", "CSV"],
            help="Choose which file formats to save the data in"
        )

    return {
        'exchange': exchange,
        'nse': {
            'circulars': nse_circulars,
            'reports': nse_reports,
            'announcements': nse_announcements,
            'bhavcopy': nse_bhavcopy
        },
        'bse': {
            'circulars': bse_circulars,
            'reports': bse_reports,
            'actions': bse_actions,
            'news': bse_news,
            'bhavcopy': bse_bhavcopy
        },
        'days': days,
        'output_format': output_format
    }


def scrape_nse_data(settings, progress_bar, status_text):
    """Scrape NSE data based on settings"""
    scraper = NSEScraper()
    results = {}

    total_tasks = sum([
        settings['nse']['circulars'],
        settings['nse']['reports'],
        settings['nse']['announcements'],
        settings['nse']['bhavcopy']
    ])

    if total_tasks == 0:
        return results

    current_task = 0

    try:
        if settings['nse']['circulars']:
            status_text.text("📄 Fetching NSE circulars...")
            circulars = scraper.scrape_circulars(days=settings['days'])
            results['nse_circulars'] = circulars
            current_task += 1
            progress_bar.progress(current_task / total_tasks)
            time.sleep(0.5)

        if settings['nse']['reports']:
            status_text.text("📊 Fetching NSE daily reports...")
            reports = scraper.scrape_daily_reports('equity')
            results['nse_reports'] = reports
            current_task += 1
            progress_bar.progress(current_task / total_tasks)
            time.sleep(0.5)

        if settings['nse']['announcements']:
            status_text.text("📢 Fetching NSE announcements...")
            announcements = scraper.scrape_announcements()
            results['nse_announcements'] = announcements
            current_task += 1
            progress_bar.progress(current_task / total_tasks)
            time.sleep(0.5)

        if settings['nse']['bhavcopy']:
            status_text.text("📈 Downloading NSE Bhavcopy...")
            bhavcopy = scraper.scrape_equity_bhavcopy()
            results['nse_bhavcopy'] = bhavcopy
            current_task += 1
            progress_bar.progress(current_task / total_tasks)
            time.sleep(0.5)

    except Exception as e:
        st.error(f"Error scraping NSE data: {e}")

    return results


def scrape_bse_data(settings, progress_bar, status_text):
    """Scrape BSE data based on settings"""
    scraper = BSEScraper()
    results = {}

    total_tasks = sum([
        settings['bse']['circulars'],
        settings['bse']['reports'],
        settings['bse']['actions'],
        settings['bse']['news'],
        settings['bse']['bhavcopy']
    ])

    if total_tasks == 0:
        return results

    current_task = 0

    try:
        if settings['bse']['circulars']:
            status_text.text("📄 Fetching BSE circulars...")
            circulars = scraper.scrape_circulars(days=settings['days'])
            results['bse_circulars'] = circulars
            current_task += 1
            progress_bar.progress(current_task / total_tasks)
            time.sleep(0.5)

        if settings['bse']['reports']:
            status_text.text("📊 Fetching BSE daily reports...")
            reports = scraper.scrape_daily_reports('market_summary')
            results['bse_reports'] = reports
            current_task += 1
            progress_bar.progress(current_task / total_tasks)
            time.sleep(0.5)

        if settings['bse']['actions']:
            status_text.text("🎯 Fetching BSE corporate actions...")
            actions = scraper.scrape_corporate_actions()
            results['bse_corporate_actions'] = actions
            current_task += 1
            progress_bar.progress(current_task / total_tasks)
            time.sleep(0.5)

        if settings['bse']['news']:
            status_text.text("📰 Fetching BSE news...")
            news = scraper.scrape_news()
            results['bse_news'] = news
            current_task += 1
            progress_bar.progress(current_task / total_tasks)
            time.sleep(0.5)

        if settings['bse']['bhavcopy']:
            status_text.text("📈 Downloading BSE Bhavcopy...")
            bhavcopy = scraper.scrape_bhavcopy()
            results['bse_bhavcopy'] = bhavcopy
            current_task += 1
            progress_bar.progress(current_task / total_tasks)
            time.sleep(0.5)

    except Exception as e:
        st.error(f"Error scraping BSE data: {e}")

    return results


def display_results(data):
    """Display scraped results in a user-friendly way"""
    if not data:
        st.warning("No data was scraped. Please select at least one data type and try again.")
        return

    st.success(f"✅ Successfully scraped {len(data)} data types!")

    # Create tabs for each data type
    tabs = st.tabs(list(data.keys()))

    for idx, (data_type, content) in enumerate(data.items()):
        with tabs[idx]:
            st.subheader(f"📋 {data_type.replace('_', ' ').title()}")

            if isinstance(content, list) and len(content) > 0:
                st.write(f"**Total records:** {len(content)}")

                # Display as DataFrame if possible
                try:
                    df = pd.DataFrame(content)
                    st.dataframe(df, use_container_width=True)

                    # Download buttons
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name=f"{data_type}_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )

                    with col2:
                        json_str = json.dumps(content, indent=2, ensure_ascii=False)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_str,
                            file_name=f"{data_type}_{datetime.now().strftime('%Y%m%d')}.json",
                            mime="application/json"
                        )

                    with col3:
                        # Excel download
                        from io import BytesIO
                        buffer = BytesIO()
                        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                            df.to_excel(writer, index=False, sheet_name=data_type[:31])

                        st.download_button(
                            label="📥 Download Excel",
                            data=buffer.getvalue(),
                            file_name=f"{data_type}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                except Exception as e:
                    st.write(content)
                    st.error(f"Could not display as table: {e}")

            elif isinstance(content, dict):
                st.json(content)

                # Download button for dict
                json_str = json.dumps(content, indent=2, ensure_ascii=False)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=f"{data_type}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

            elif isinstance(content, list) and len(content) == 0:
                st.info("No data available for the selected time period.")

            else:
                st.write(content)


def main():
    """Main application"""
    display_header()

    # Get settings from sidebar
    settings = sidebar_settings()

    # Main content area
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        start_button = st.button("🚀 Start Scraping", type="primary", use_container_width=True)

    # Show what will be scraped
    with st.expander("📋 Summary of Selected Data"):
        st.write(f"**Exchange:** {settings['exchange']}")
        st.write(f"**Time Range:** Last {settings['days']} days")
        st.write(f"**Output Formats:** {', '.join(settings['output_format'])}")

        if settings['exchange'] in ["Both NSE & BSE", "NSE Only"]:
            st.write("**NSE Data:**")
            nse_items = [k for k, v in settings['nse'].items() if v]
            if nse_items:
                for item in nse_items:
                    st.write(f"  - {item.replace('_', ' ').title()}")
            else:
                st.write("  - None selected")

        if settings['exchange'] in ["Both NSE & BSE", "BSE Only"]:
            st.write("**BSE Data:**")
            bse_items = [k for k, v in settings['bse'].items() if v]
            if bse_items:
                for item in bse_items:
                    st.write(f"  - {item.replace('_', ' ').title()}")
            else:
                st.write("  - None selected")

    # Start scraping when button is clicked
    if start_button:
        # Check if at least one option is selected
        has_selection = any(settings['nse'].values()) or any(settings['bse'].values())

        if not has_selection:
            st.error("❌ Please select at least one data type to scrape!")
            return

        # Progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()

        st.info("⏳ Scraping in progress... This may take a few minutes.")

        # Scrape data
        all_results = {}

        if settings['exchange'] in ["Both NSE & BSE", "NSE Only"]:
            status_text.text("🔄 Scraping NSE data...")
            nse_results = scrape_nse_data(settings, progress_bar, status_text)
            all_results.update(nse_results)

        if settings['exchange'] in ["Both NSE & BSE", "BSE Only"]:
            status_text.text("🔄 Scraping BSE data...")
            bse_results = scrape_bse_data(settings, progress_bar, status_text)
            all_results.update(bse_results)

        # Complete
        progress_bar.progress(1.0)
        status_text.text("✅ Scraping completed!")

        # Store in session state
        st.session_state.scraped_data = all_results

        # Display results
        st.divider()
        st.header("📊 Results")
        display_results(all_results)

    # Display previously scraped data if available
    elif st.session_state.scraped_data:
        st.divider()
        st.header("📊 Previous Results")
        st.info("Showing results from your last scraping session. Click 'Start Scraping' to fetch new data.")
        display_results(st.session_state.scraped_data)

    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
    <p>Made with ❤️ for stock market data enthusiasts</p>
    <p><small>Data is scraped from official NSE and BSE websites. Always verify critical information with official sources.</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
