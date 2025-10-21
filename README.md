# NSE/BSE Webscraper

A comprehensive Python webscraper for extracting circulars, daily reports, announcements, and other data from the National Stock Exchange (NSE) and Bombay Stock Exchange (BSE) websites.

## Features

### NSE (National Stock Exchange)
- Corporate circulars and announcements
- Daily equity reports
- Market indices data
- Equity Bhavcopy (daily market report)
- Latest announcements

### BSE (Bombay Stock Exchange)
- Corporate circulars and announcements
- Daily market reports
- Corporate actions
- News updates
- Equity Bhavcopy (ZIP format)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
.
├── main.py              # Main script with CLI interface
├── nse_scraper.py       # NSE scraper implementation
├── bse_scraper.py       # BSE scraper implementation
├── base_scraper.py      # Base scraper class with common functionality
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
├── data/               # Output directory (created automatically)
└── logs/               # Log files directory (created automatically)
```

## Usage

### Basic Usage

Run the scraper using the main script:

```bash
python main.py --exchange <nse|bse|both> [options]
```

### Command Line Arguments

- `--exchange`: Choose exchange (nse, bse, or both) - **default: both**
- `--circulars`: Scrape circulars/announcements
- `--reports`: Scrape daily reports
- `--announcements`: Scrape announcements (NSE only)
- `--corporate-actions`: Scrape corporate actions (BSE only)
- `--news`: Scrape news (BSE only)
- `--bhavcopy`: Download Bhavcopy (daily market report)
- `--all`: Scrape all available data
- `--days`: Number of days to fetch data for (default: 7)

### Examples

1. **Scrape NSE circulars and reports:**
```bash
python main.py --exchange nse --circulars --reports
```

2. **Scrape BSE circulars for the last 30 days:**
```bash
python main.py --exchange bse --circulars --days 30
```

3. **Scrape everything from both exchanges:**
```bash
python main.py --exchange both --all
```

4. **Scrape specific items from NSE:**
```bash
python main.py --exchange nse --circulars --announcements --bhavcopy
```

5. **Get help:**
```bash
python main.py --help
```

### Using Individual Scrapers

You can also use the scrapers independently in your Python code:

#### NSE Scraper Example:
```python
from nse_scraper import NSEScraper

# Initialize scraper
scraper = NSEScraper()

# Scrape circulars
circulars = scraper.scrape_circulars(days=7)

# Scrape daily reports
reports = scraper.scrape_daily_reports('equity')

# Download Bhavcopy
bhavcopy = scraper.scrape_equity_bhavcopy()

# Save to file
scraper.save_to_file(circulars, 'nse_circulars.json', 'json')
```

#### BSE Scraper Example:
```python
from bse_scraper import BSEScraper

# Initialize scraper
scraper = BSEScraper()

# Scrape circulars
circulars = scraper.scrape_circulars(days=7)

# Scrape daily reports
reports = scraper.scrape_daily_reports('market_summary')

# Scrape corporate actions
actions = scraper.scrape_corporate_actions()

# Save to file
scraper.save_to_file(circulars, 'bse_circulars.json', 'json')
```

## Output

All scraped data is saved to the `data/` directory in multiple formats:

- **JSON**: Structured data with complete information
- **CSV**: Tabular format for easy analysis in Excel/spreadsheet applications

Log files are stored in the `logs/` directory with detailed information about the scraping process.

## Configuration

You can modify settings in `config.py`:

- `REQUEST_TIMEOUT`: HTTP request timeout (default: 30 seconds)
- `RETRY_ATTEMPTS`: Number of retry attempts for failed requests (default: 3)
- `RETRY_DELAY`: Delay between retries (default: 2 seconds)
- `RATE_LIMIT_DELAY`: Delay between requests to avoid overwhelming servers (default: 1 second)
- `LOG_LEVEL`: Logging level (default: INFO)

## Features & Capabilities

### Error Handling
- Automatic retry mechanism for failed requests
- Comprehensive error logging
- Graceful degradation when data is unavailable

### Rate Limiting
- Built-in delays between requests to avoid overwhelming servers
- Respects website terms of service

### Data Formats
- Multiple output formats (JSON, CSV)
- Structured data with timestamps
- Preserves original data integrity

### Logging
- Detailed logs for debugging
- Separate log files for NSE and BSE scrapers
- Console output for real-time monitoring

## Important Notes

1. **Website Changes**: Stock exchange websites may change their structure. If the scraper stops working, the selectors and URLs may need to be updated.

2. **Rate Limiting**: Be respectful of the websites. The scraper includes rate limiting, but avoid running it too frequently.

3. **Legal Compliance**: Ensure you comply with the terms of service of NSE and BSE websites. This scraper is for educational and research purposes.

4. **Data Accuracy**: Always verify critical data with official sources. Web scraping may not capture all information accurately.

5. **Network Requirements**: The scraper requires internet access and the NSE/BSE websites must be accessible from your network.

## Troubleshooting

### Common Issues

1. **Connection Errors**:
   - Check your internet connection
   - Verify that NSE/BSE websites are accessible
   - Check if your network has firewall restrictions

2. **No Data Returned**:
   - The website structure may have changed
   - Data may not be available for the requested period
   - Check the log files for detailed error messages

3. **Import Errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Activate your virtual environment if using one

4. **Permission Errors**:
   - Ensure you have write permissions for the `data/` and `logs/` directories

## Dependencies

- **requests**: HTTP library for making web requests
- **beautifulsoup4**: HTML parsing library
- **selenium**: Browser automation (for JavaScript-heavy pages)
- **lxml**: XML/HTML parser
- **pandas**: Data manipulation and CSV export
- **python-dotenv**: Environment variable management

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is provided as-is for educational and research purposes.

## Disclaimer

This scraper is not affiliated with or endorsed by NSE or BSE. Use responsibly and in accordance with the websites' terms of service. The authors are not responsible for any misuse of this tool.

## Support

For issues, questions, or suggestions, please open an issue on the project repository.
