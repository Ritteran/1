"""
NSE (National Stock Exchange) webscraper for circulars and daily reports
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import json
from base_scraper import BaseScraper
import config


class NSEScraper(BaseScraper):
    """Scraper for NSE India website"""

    def __init__(self):
        super().__init__("NSE_Scraper")
        self.base_url = config.NSE_BASE_URL

    def scrape_circulars(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Scrape circulars from NSE

        Args:
            days: Number of days to fetch circulars for (default: 7)

        Returns:
            List of circular dictionaries
        """
        self.logger.info(f"Scraping NSE circulars for the last {days} days")

        circulars = []

        # NSE Corporate Announcements API endpoint
        api_url = f"{self.base_url}/api/corporates-corporateActions"

        try:
            response = self.fetch_page(api_url)
            if not response:
                self.logger.error("Failed to fetch NSE circulars")
                return circulars

            try:
                data = response.json()
                if isinstance(data, list):
                    for item in data:
                        circular = {
                            'date': item.get('exDate', ''),
                            'company': item.get('company', ''),
                            'symbol': item.get('symbol', ''),
                            'subject': item.get('subject', ''),
                            'purpose': item.get('purpose', ''),
                            'source': 'NSE',
                            'scraped_at': datetime.now().isoformat()
                        }
                        circulars.append(circular)

                self.logger.info(f"Successfully scraped {len(circulars)} NSE circulars")

            except json.JSONDecodeError:
                self.logger.warning("Response is not JSON, attempting HTML parsing")
                circulars = self._scrape_circulars_html(response.text)

        except Exception as e:
            self.logger.error(f"Error scraping NSE circulars: {e}")

        return circulars

    def _scrape_circulars_html(self, html_content: str) -> List[Dict[str, Any]]:
        """
        Fallback method to scrape circulars from HTML

        Args:
            html_content: HTML content to parse

        Returns:
            List of circular dictionaries
        """
        circulars = []
        soup = self.parse_html(html_content)

        # Look for tables or divs containing circular information
        tables = soup.find_all('table')

        for table in tables:
            rows = table.find_all('tr')[1:]  # Skip header row
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    circular = {
                        'date': cols[0].get_text(strip=True) if len(cols) > 0 else '',
                        'company': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                        'subject': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                        'source': 'NSE',
                        'scraped_at': datetime.now().isoformat()
                    }
                    circulars.append(circular)

        return circulars

    def scrape_daily_reports(self, report_type: str = 'equity') -> List[Dict[str, Any]]:
        """
        Scrape daily reports from NSE

        Args:
            report_type: Type of report (equity, derivatives, etc.)

        Returns:
            List of report dictionaries
        """
        self.logger.info(f"Scraping NSE daily reports for {report_type}")

        reports = []

        # NSE Market Data API endpoints
        endpoints = {
            'equity': f"{self.base_url}/api/equity-stockIndices",
            'derivatives': f"{self.base_url}/api/option-chain-indices",
            'market_status': f"{self.base_url}/api/marketStatus",
        }

        url = endpoints.get(report_type, endpoints['equity'])

        try:
            response = self.fetch_page(url)
            if not response:
                self.logger.error(f"Failed to fetch NSE daily reports for {report_type}")
                return reports

            try:
                data = response.json()

                report = {
                    'report_type': report_type,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'data': data,
                    'source': 'NSE',
                    'scraped_at': datetime.now().isoformat()
                }
                reports.append(report)

                self.logger.info(f"Successfully scraped NSE {report_type} report")

            except json.JSONDecodeError:
                self.logger.error("Failed to parse JSON response")

        except Exception as e:
            self.logger.error(f"Error scraping NSE daily reports: {e}")

        return reports

    def scrape_equity_bhavcopy(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Scrape NSE Equity Bhavcopy (daily market report)

        Args:
            date: Date in format DDMMMYYYY (e.g., 21OCT2023). If None, uses today's date

        Returns:
            Dictionary containing bhavcopy data
        """
        if date is None:
            date = datetime.now().strftime('%d%b%Y').upper()

        self.logger.info(f"Scraping NSE Equity Bhavcopy for {date}")

        # NSE Bhavcopy URL format
        # Example: https://www.nseindia.com/products/content/sec_bhavdata_full.csv
        bhavcopy_url = f"{self.base_url}/products/content/sec_bhavdata_full.csv"

        try:
            response = self.fetch_page(bhavcopy_url)
            if response:
                bhavcopy_data = {
                    'date': date,
                    'content': response.text,
                    'source': 'NSE',
                    'scraped_at': datetime.now().isoformat()
                }

                # Save CSV data
                filename = f"nse_bhavcopy_{date}.csv"
                self.save_to_file(response.text, filename, 'txt')

                self.logger.info(f"Successfully scraped NSE Bhavcopy for {date}")
                return bhavcopy_data

        except Exception as e:
            self.logger.error(f"Error scraping NSE Bhavcopy: {e}")

        return {}

    def scrape_announcements(self, index: str = 'equities') -> List[Dict[str, Any]]:
        """
        Scrape latest announcements from NSE

        Args:
            index: Index type (equities, fno, etc.)

        Returns:
            List of announcement dictionaries
        """
        self.logger.info(f"Scraping NSE announcements for {index}")

        announcements = []

        # NSE Latest Announcements
        url = f"{self.base_url}/companies-listing/corporate-filings-announcements"

        try:
            response = self.fetch_page(url)
            if not response:
                return announcements

            soup = self.parse_html(response.text)

            # Find announcement sections
            announcement_divs = soup.find_all('div', class_=['announcement', 'corporate-announcement'])

            for div in announcement_divs:
                announcement = {
                    'title': div.find('h3').get_text(strip=True) if div.find('h3') else '',
                    'date': div.find('span', class_='date').get_text(strip=True) if div.find('span', class_='date') else '',
                    'content': div.get_text(strip=True),
                    'source': 'NSE',
                    'scraped_at': datetime.now().isoformat()
                }
                announcements.append(announcement)

            self.logger.info(f"Successfully scraped {len(announcements)} NSE announcements")

        except Exception as e:
            self.logger.error(f"Error scraping NSE announcements: {e}")

        return announcements


if __name__ == "__main__":
    # Example usage
    scraper = NSEScraper()

    # Scrape circulars
    circulars = scraper.scrape_circulars(days=7)
    if circulars:
        scraper.save_to_file(circulars, 'nse_circulars.json', 'json')

    # Scrape daily reports
    reports = scraper.scrape_daily_reports('equity')
    if reports:
        scraper.save_to_file(reports, 'nse_daily_reports.json', 'json')

    # Scrape announcements
    announcements = scraper.scrape_announcements()
    if announcements:
        scraper.save_to_file(announcements, 'nse_announcements.json', 'json')
