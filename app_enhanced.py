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
from pathlib import Path
from io import BytesIO

# Import scrapers and processor
from nse_scraper import NSEScraper
from bse_scraper import BSEScraper
from data_processor import DataProcessor
import config

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


def main():
    """Main application"""

    # Header
    st.markdown('<h1 class="main-header">📈 NSE/BSE Market Data Application</h1>',
                unsafe_allow_html=True)

    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📥 Scraper",
        "📂 Data Loader",
        "⚙️ Processor",
        "📊 Visualization",
        "📈 Analytics"
    ])

    with tab1:
        scraper_tab()

    with tab2:
        data_loader_tab()

    with tab3:
        data_processor_tab()

    with tab4:
        visualization_tab()

    with tab5:
        analytics_tab()

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
