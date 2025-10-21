"""
Configuration file for NSE/BSE webscraper
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# NSE Configuration
NSE_BASE_URL = "https://www.nseindia.com"
NSE_CIRCULARS_URL = f"{NSE_BASE_URL}/companies-listing/corporate-filings-announcements"
NSE_DAILY_REPORTS_URL = f"{NSE_BASE_URL}/report-detail"

# BSE Configuration
BSE_BASE_URL = "https://www.bseindia.com"
BSE_CIRCULARS_URL = f"{BSE_BASE_URL}/corporates/ann.aspx"
BSE_DAILY_REPORTS_URL = f"{BSE_BASE_URL}/markets/MarketInfo/DispNews.aspx"

# Headers to mimic browser requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

# Request settings
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds

# Rate limiting
RATE_LIMIT_DELAY = 1  # seconds between requests

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
