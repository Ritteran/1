# 📈 NSE/BSE Stock Market Scraper

A user-friendly tool for extracting circulars, daily reports, announcements, and other data from the National Stock Exchange (NSE) and Bombay Stock Exchange (BSE) websites.

**✨ NEW: Easy-to-use Web Interface - No coding required!**

> **📄 Want to see what this tool can do?** Just open `index.html` in your browser for a beautiful interactive guide!

---

## 🚀 Quick Start (For Non-Technical Users)

### Option 1: Open the HTML Guide (Easiest!)
Simply double-click the `index.html` file to open it in your web browser. You'll see:
- Beautiful visual guide
- Interactive command generator
- Step-by-step instructions
- Feature showcase

### Option 2: Launch the Web App Directly

#### Step 1: Install Python

If you don't have Python installed:
- **Windows/Mac**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: Python is usually pre-installed

#### Step 2: Download This Project

Download and extract the project files to a folder on your computer.

#### Step 3: Launch the Application

**On Windows:**
1. Double-click the `start.bat` file
2. Wait for the installation to complete (first time only)
3. Your web browser will open automatically

**On Mac/Linux:**
1. Open Terminal in the project folder
2. Run: `./start.sh`
3. Your web browser will open automatically

#### Step 4: Use the Web Interface

1. **Select Exchange**: Choose NSE, BSE, or both
2. **Select Data Types**: Check the boxes for what you want
3. **Set Time Range**: Choose how many days of data to fetch
4. **Click "Start Scraping"**: Wait for the data to be collected
5. **Download Your Data**: Click the download buttons to get your files

**That's it! No coding required!**

---

## 📸 Screenshots

The web interface provides:
- ✅ Simple checkboxes to select what data you want
- ✅ Progress bar showing scraping status
- ✅ Preview of scraped data in tables
- ✅ One-click download buttons (CSV, JSON, Excel)
- ✅ No technical knowledge needed

---

## 📊 What Data Can You Get?

### NSE (National Stock Exchange)
- 📄 **Circulars & Announcements**: Corporate filings and announcements
- 📊 **Daily Market Reports**: Equity market data and indices
- 📢 **Latest Announcements**: Breaking news and updates
- 📈 **Bhavcopy**: Complete daily market report

### BSE (Bombay Stock Exchange)
- 📄 **Circulars & Announcements**: Corporate filings and announcements
- 📊 **Daily Market Reports**: Market summary and statistics
- 🎯 **Corporate Actions**: Dividends, splits, bonuses, etc.
- 📰 **News Updates**: Latest market news
- 📈 **Bhavcopy**: Complete daily market report (ZIP)

---

## 💻 For Advanced Users: Command Line Interface

If you prefer the command line or want to automate tasks:

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### CLI Usage

```bash
# Scrape everything from both exchanges
python main.py --exchange both --all

# Scrape NSE circulars and reports
python main.py --exchange nse --circulars --reports

# Scrape BSE data for last 30 days
python main.py --exchange bse --circulars --days 30

# Get help
python main.py --help
```

### Command Line Options

- `--exchange`: Choose exchange (nse, bse, or both)
- `--circulars`: Scrape circulars/announcements
- `--reports`: Scrape daily reports
- `--announcements`: Scrape announcements (NSE only)
- `--corporate-actions`: Scrape corporate actions (BSE only)
- `--news`: Scrape news (BSE only)
- `--bhavcopy`: Download Bhavcopy
- `--all`: Scrape all available data
- `--days`: Number of days (default: 7)

---

## 👨‍💻 For Developers: Using as a Python Library

You can integrate the scrapers into your own Python code:

### NSE Scraper Example:
```python
from nse_scraper import NSEScraper

# Initialize scraper
scraper = NSEScraper()

# Scrape circulars
circulars = scraper.scrape_circulars(days=7)

# Scrape daily reports
reports = scraper.scrape_daily_reports('equity')

# Save to file
scraper.save_to_file(circulars, 'nse_circulars.json', 'json')
```

### BSE Scraper Example:
```python
from bse_scraper import BSEScraper

# Initialize scraper
scraper = BSEScraper()

# Scrape circulars
circulars = scraper.scrape_circulars(days=7)

# Scrape corporate actions
actions = scraper.scrape_corporate_actions()

# Save to file
scraper.save_to_file(circulars, 'bse_circulars.csv', 'csv')
```

See `example.py` for more examples.

---

## 📁 Project Structure

```
.
├── start.sh             # Launcher for Mac/Linux (double-click to start)
├── start.bat            # Launcher for Windows (double-click to start)
├── app.py               # Web interface (Streamlit GUI)
├── main.py              # Command line interface
├── nse_scraper.py       # NSE scraper implementation
├── bse_scraper.py       # BSE scraper implementation
├── base_scraper.py      # Base scraper class
├── config.py            # Configuration settings
├── example.py           # Example usage scripts
├── requirements.txt     # Python dependencies
├── data/                # Output directory (auto-created)
└── logs/                # Log files (auto-created)
```

---

## 📂 Output Files

All scraped data is saved to the `data/` folder in multiple formats:

- **JSON**: Complete structured data
- **CSV**: Open in Excel or Google Sheets
- **Excel**: Native Excel format (.xlsx)

You can also download files directly from the web interface!

---

## ⚙️ Configuration

Advanced users can modify `config.py` to customize:
- Request timeouts
- Retry attempts
- Rate limiting delays
- Log levels
- Output directories

---

## ❓ Troubleshooting

### Application won't start
1. Make sure Python is installed: Run `python --version` in terminal
2. Try running the installer manually: `pip install -r requirements.txt`
3. Check that you have internet access

### No data is returned
1. Check your internet connection
2. Verify NSE/BSE websites are accessible
3. Check the log files in the `logs/` folder
4. The website structure may have changed (check for updates)

### Browser doesn't open automatically
- Manually open your browser and go to: `http://localhost:8501`

### Excel export not working
- Make sure all dependencies are installed: `pip install -r requirements.txt`

---

## 🔐 Important Notes

1. **Data Accuracy**: Always verify critical data with official sources
2. **Legal Compliance**: Use responsibly and follow NSE/BSE terms of service
3. **Rate Limiting**: Don't run the scraper too frequently
4. **Website Changes**: Exchange websites may update their structure
5. **Educational Use**: This tool is for educational and research purposes

---

## 🛠️ Technical Features

### For Developers
- Object-oriented architecture with inheritance
- Comprehensive error handling and retry logic
- Rate limiting to respect server resources
- Detailed logging for debugging
- Multiple output format support
- Configurable parameters
- Clean separation of concerns

### Reliability
- ✅ Automatic retry on failures
- ✅ Graceful error handling
- ✅ Comprehensive logging
- ✅ Rate limiting built-in
- ✅ Session management
- ✅ Data validation

---

## 📦 Dependencies

- **streamlit**: Web interface framework
- **requests**: HTTP library
- **beautifulsoup4**: HTML parsing
- **pandas**: Data manipulation
- **lxml**: XML/HTML parser
- **plotly**: Data visualization
- **xlsxwriter**: Excel file creation

Full list in `requirements.txt`

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Submit bug reports
- Suggest new features
- Submit pull requests
- Improve documentation

---

## 📜 License

This project is provided as-is for educational and research purposes.

---

## ⚠️ Disclaimer

This scraper is not affiliated with or endorsed by NSE or BSE. Use responsibly and in accordance with the websites' terms of service. The authors are not responsible for any misuse of this tool.

---

## 💡 Tips for Best Results

1. **Start Small**: Begin with a short time range (7 days) to test
2. **Peak Hours**: Avoid scraping during market hours for better performance
3. **Save Regular**: Download your data immediately after scraping
4. **Check Logs**: Review log files if something doesn't work
5. **Update Regularly**: Keep the scraper updated for website changes

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on the project repository
- Check the logs folder for error details
- Review the troubleshooting section above

---

**Made with ❤️ for stock market enthusiasts**

*Remember: This tool makes data collection easy, but always verify important information with official sources!*
