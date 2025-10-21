"""
Base scraper class with common functionality
"""

import logging
import time
from pathlib import Path
from typing import Optional, Dict, Any
import requests
from bs4 import BeautifulSoup
import config


class BaseScraper:
    """Base class for NSE and BSE scrapers"""

    def __init__(self, name: str):
        self.name = name
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up logging configuration"""
        logger = logging.getLogger(self.name)
        logger.setLevel(getattr(logging, config.LOG_LEVEL))

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(config.LOG_FORMAT)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler
        log_file = config.LOGS_DIR / f"{self.name}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def fetch_page(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[requests.Response]:
        """
        Fetch a webpage with retry logic

        Args:
            url: URL to fetch
            params: Optional query parameters

        Returns:
            Response object or None if all retries failed
        """
        for attempt in range(config.RETRY_ATTEMPTS):
            try:
                self.logger.debug(f"Fetching {url} (attempt {attempt + 1}/{config.RETRY_ATTEMPTS})")
                response = self.session.get(
                    url,
                    params=params,
                    timeout=config.REQUEST_TIMEOUT
                )
                response.raise_for_status()

                # Rate limiting
                time.sleep(config.RATE_LIMIT_DELAY)

                return response

            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < config.RETRY_ATTEMPTS - 1:
                    time.sleep(config.RETRY_DELAY * (attempt + 1))
                else:
                    self.logger.error(f"All retry attempts failed for {url}")

        return None

    def parse_html(self, html_content: str) -> BeautifulSoup:
        """
        Parse HTML content using BeautifulSoup

        Args:
            html_content: HTML string to parse

        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html_content, 'lxml')

    def save_to_file(self, data: Any, filename: str, file_format: str = 'json'):
        """
        Save data to file

        Args:
            data: Data to save
            filename: Output filename
            file_format: File format (json, csv, txt)
        """
        import json
        import pandas as pd

        output_path = config.DATA_DIR / filename

        try:
            if file_format == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

            elif file_format == 'csv' and isinstance(data, (list, dict)):
                df = pd.DataFrame(data)
                df.to_csv(output_path, index=False, encoding='utf-8')

            elif file_format == 'txt':
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(str(data))

            self.logger.info(f"Data saved to {output_path}")

        except Exception as e:
            self.logger.error(f"Failed to save data to {output_path}: {e}")

    def scrape_circulars(self):
        """To be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement scrape_circulars()")

    def scrape_daily_reports(self):
        """To be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement scrape_daily_reports()")
