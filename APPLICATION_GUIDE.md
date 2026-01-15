# 📱 NSE/BSE Market Data Application Guide

## Complete Desktop Application for Stock Market Data

This is a full-featured desktop application that allows you to scrape, process, analyze, and visualize NSE and BSE stock market data - all through an intuitive graphical interface!

---

## 🚀 Quick Start

### Windows Users:
Double-click **`start_app.bat`**

### Mac/Linux Users:
Run **`./start_app.sh`** in Terminal

Your web browser will open automatically with the application!

---

## 📋 Application Features

### 1. 📥 Data Scraper
**What it does:** Downloads fresh data from NSE and BSE websites

**Features:**
- Select NSE, BSE, or both exchanges
- Choose specific data types (circulars, reports, news, etc.)
- Set custom time ranges (1-90 days)
- Real-time progress indicators
- Automatic file saving

**How to use:**
1. Go to the "Scraper" tab
2. Select your options in the left panel
3. Click "Start Scraping"
4. Wait for completion
5. Download or proceed to process the data

---

### 2. 📂 Data Loader
**What it does:** Loads and previews data files

**Features:**
- Load from previously scraped files
- Upload your own data files (JSON, CSV, Excel)
- Instant data preview
- Column information and statistics
- Memory usage tracking

**How to use:**
1. Go to the "Data Loader" tab
2. Select a file from the dropdown
3. Click "Load File"
4. View the data preview

**Supported formats:**
- JSON (.json)
- CSV (.csv)
- Excel (.xlsx, .xls)

---

### 3. ⚙️ Data Processor
**What it does:** Filters, searches, and transforms your data

**Processing Options:**

#### 🧹 Data Cleaning
- Removes duplicate records
- Strips whitespace
- Standardizes date formats
- Removes empty rows

#### 📅 Date Filtering
- Filter by date range
- Automatic date detection
- Visual date picker

#### 🔍 Keyword Search
- Search in specific columns or all columns
- Multiple keywords (comma-separated)
- Case-sensitive or case-insensitive
- Regex pattern support

#### 🏢 Company Filtering
- Filter by company names
- Filter by stock symbols
- Multiple companies at once

#### 💾 Export Options
Export your processed data in:
- CSV (for Excel/Google Sheets)
- JSON (for developers)
- Excel (native .xlsx format)

**How to use:**
1. Load data first (Data Loader tab)
2. Go to "Processor" tab
3. Configure filters in left panel
4. Click "Apply Filters"
5. Preview results
6. Download processed data

---

### 4. 📊 Data Visualization
**What it does:** Creates interactive charts and graphs

**Available Visualizations:**

#### 📈 Time Series
- Activity over time
- Daily, weekly, monthly trends
- Interactive hover tooltips
- Zoom and pan features

#### 📊 Bar Charts
- Distribution by category
- Top N items
- Horizontal or vertical

#### 🥧 Pie Charts
- Category distribution
- Percentage breakdown
- Interactive slices

#### 📉 Trend Analysis
- Detect increasing/decreasing trends
- Peak days analysis
- Quiet periods identification
- Overall trend direction

#### 🔥 Heatmaps
- Activity by day of week
- Weekly patterns
- Color-coded intensity

**How to use:**
1. Load data first
2. Go to "Visualization" tab
3. Select chart type
4. Choose columns for analysis
5. Interact with the charts (zoom, hover, filter)

---

### 5. 📈 Advanced Analytics
**What it does:** Deep insights and data quality analysis

**Analytics Features:**

#### 📊 Summary Statistics
- Total records count
- Column count
- Unique companies
- Date range coverage
- Category breakdown

#### 📋 Category Analysis
- Automatic categorization
- Distribution charts
- Top categories

#### ✅ Data Quality
- Missing values detection
- Duplicate detection and removal
- Column completeness
- Data type validation

#### 🔍 Advanced Search
- Multi-column search
- Instant results
- Highlighted matches
- Search across all fields

**How to use:**
1. Load your data
2. Go to "Analytics" tab
3. Review automatic insights
4. Use advanced search for specific queries
5. Fix data quality issues

---

## 💡 Complete Workflow Example

### Scenario: Finding all dividend announcements from Reliance Industries

1. **Scrape Data**
   - Go to "Scraper" tab
   - Select "BSE Only"
   - Check "Corporate Actions"
   - Set days to 90
   - Click "Start Scraping"

2. **Load Data**
   - Go to "Data Loader" tab
   - Select "bse_corporate_actions.json"
   - Click "Load File"

3. **Process Data**
   - Go to "Processor" tab
   - In "Company Filter", type: "RELIANCE"
   - In "Keyword Filter", search in "purpose" column for: "dividend"
   - Click "Apply Filters"

4. **Visualize**
   - Go to "Visualization" tab
   - Select "Time Series"
   - View dividend announcements over time

5. **Export**
   - In "Processor" tab
   - Click "Download Excel"
   - Open in Microsoft Excel

---

## 🎯 Tips and Tricks

### For Best Results:

1. **Start with Recent Data**
   - Use 7-30 days for initial tests
   - Expand range once you're comfortable

2. **Clean Before Processing**
   - Always enable "Clean Data" checkbox
   - Removes duplicates automatically
   - Standardizes formats

3. **Use Multiple Filters**
   - Combine date + keyword + company filters
   - Narrow down to exactly what you need

4. **Save Processed Data**
   - Download your filtered results
   - Reuse without re-scraping
   - Faster analysis

5. **Explore Visualizations**
   - Try different chart types
   - Look for patterns and trends
   - Use heatmaps for weekly patterns

### Keyboard Shortcuts:

- **Ctrl + R**: Refresh the page
- **Ctrl + S**: (in browser) Save chart as image
- **Ctrl + F**: Find in current page

---

## 🔧 Troubleshooting

### Application won't start
**Solution:**
- Ensure Python 3.8+ is installed
- Run: `pip install -r requirements.txt`
- Check internet connection

### No data appearing after scraping
**Solution:**
- Check the `logs/` folder for errors
- Verify NSE/BSE websites are accessible
- Try shorter time ranges
- Check internet connectivity

### Charts not displaying
**Solution:**
- Ensure data has date columns
- Check that data is not empty
- Try different chart types
- Refresh the page

### File upload fails
**Solution:**
- Check file format (JSON, CSV, Excel only)
- Ensure file is not corrupted
- Try smaller files first
- Check file permissions

### Slow performance
**Solution:**
- Process smaller datasets
- Close unused browser tabs
- Restart the application
- Filter data before visualizing

---

## 📊 Understanding Your Data

### NSE Data Structure:
- **Circulars**: company, symbol, subject, date, purpose
- **Reports**: market indices, equity data, derivatives
- **Announcements**: title, content, date

### BSE Data Structure:
- **Circulars**: company, category, subject, date, attachment_link
- **Corporate Actions**: company, security_code, purpose, ex_date, record_date
- **News**: title, category, content, link, date

### Date Formats:
The application automatically detects and converts various date formats:
- YYYY-MM-DD (2024-01-15)
- DD/MM/YYYY (15/01/2024)
- DD-MMM-YYYY (15-JAN-2024)

---

## 💾 File Management

### Where Files are Saved:
- **Scraped Data**: `data/` folder
- **Logs**: `logs/` folder
- **Downloads**: Your browser's download folder

### File Naming:
- Format: `source_type_YYYYMMDD.ext`
- Example: `nse_circulars_20240115.csv`

### Managing Disk Space:
- Old files are NOT automatically deleted
- Manually clean the `data/` folder periodically
- JSON files are larger than CSV
- Excel files are largest

---

## 🎓 Advanced Features

### Custom Date Ranges:
- Click calendar icon to pick specific dates
- Combine with other filters
- See results update in real-time

### Regular Expressions:
- Use in keyword search
- Example: `"^RIL"` - starts with RIL
- Example: `"dividend|bonus"` - dividend OR bonus

### Data Export:
- CSV: Best for Excel analysis
- JSON: Best for programming
- Excel: Best for non-technical users

### Batch Processing:
1. Scrape multiple exchanges
2. Load each separately
3. Process and export
4. Merge in Excel if needed

---

## 📱 Accessibility

### Browser Compatibility:
- ✅ Chrome/Chromium (Recommended)
- ✅ Firefox
- ✅ Edge
- ✅ Safari
- ⚠️ Internet Explorer (Not supported)

### Screen Readers:
- Application supports ARIA labels
- Use Tab to navigate
- Screen reader friendly

### Mobile Devices:
- Responsive design
- Works on tablets
- Limited on phones (use desktop for best experience)

---

## 🆘 Getting Help

### Built-in Help:
- Hover over any (?) icon
- Read the info boxes
- Check tab descriptions

### Documentation:
- **This Guide**: Complete feature documentation
- **README.md**: Installation and setup
- **QUICK_START.md**: Beginner guide

### Support:
- Check `logs/` folder for error details
- Review the Troubleshooting section
- Open an issue on GitHub

---

## 🎉 You're Ready!

This application gives you complete control over NSE and BSE data:

✅ **No coding required**
✅ **Point and click interface**
✅ **Real-time visualizations**
✅ **Professional exports**
✅ **Advanced analytics**

**Start exploring your stock market data today!**

---

*Made with ❤️ for data enthusiasts | Version 2.0 - Enhanced Application*
