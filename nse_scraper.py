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

    def scrape_equity_securities(self) -> List[Dict[str, Any]]:
        """
        Scrape equity securities/instruments list from NSE

        Returns:
            List of equity securities with details
        """
        self.logger.info("Scraping NSE equity securities list")

        securities = []

        # NSE Equity Securities API endpoint
        # This typically provides the full list of tradeable securities
        api_url = f"{self.base_url}/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O"

        # Alternative URLs to try
        alternative_urls = [
            f"{self.base_url}/api/equity-stockIndices?index=NIFTY%2050",
            f"{self.base_url}/api/equity-stockIndices?index=NIFTY%20500",
            f"{self.base_url}/api/allIndices",
            f"{self.base_url}/api/equity-master",
            f"{self.base_url}/api/master-quote",
        ]

        # Try to get security master list
        try:
            # First, try to get the main page to establish session
            session_response = self.fetch_page(f"{self.base_url}/market-data/live-equity-market")

            # Now try the API endpoint
            response = self.fetch_page(api_url)

            if response:
                try:
                    data = response.json()

                    # Handle different response structures
                    if isinstance(data, dict):
                        # Check for 'data' key
                        if 'data' in data:
                            stock_data = data['data']
                        elif 'stocks' in data:
                            stock_data = data['stocks']
                        else:
                            stock_data = [data]
                    else:
                        stock_data = data

                    # Parse security information
                    for item in stock_data:
                        if isinstance(item, dict):
                            security = {
                                'symbol': item.get('symbol', ''),
                                'company_name': item.get('meta', {}).get('companyName', '') if 'meta' in item else item.get('companyName', ''),
                                'industry': item.get('meta', {}).get('industry', '') if 'meta' in item else item.get('industry', ''),
                                'isin': item.get('meta', {}).get('isin', '') if 'meta' in item else item.get('isin', ''),
                                'last_price': item.get('lastPrice', 0),
                                'change': item.get('change', 0),
                                'pChange': item.get('pChange', 0),
                                'previous_close': item.get('previousClose', 0),
                                'open': item.get('open', 0),
                                'close': item.get('close', 0),
                                'year_high': item.get('yearHigh', 0),
                                'year_low': item.get('yearLow', 0),
                                'source': 'NSE',
                                'scraped_at': datetime.now().isoformat()
                            }
                            securities.append(security)

                    self.logger.info(f"Successfully scraped {len(securities)} equity securities")

                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON response: {e}")
                    # Try alternative endpoints
                    for alt_url in alternative_urls:
                        self.logger.info(f"Trying alternative endpoint: {alt_url}")
                        try:
                            alt_response = self.fetch_page(alt_url)
                            if alt_response:
                                alt_data = alt_response.json()
                                self.logger.info(f"Successfully fetched from alternative endpoint")
                                # Process alternative data structure
                                securities = self._parse_securities_data(alt_data)
                                if securities:
                                    break
                        except Exception as alt_e:
                            self.logger.debug(f"Alternative endpoint failed: {alt_e}")
                            continue

        except Exception as e:
            self.logger.error(f"Error scraping equity securities: {e}")
            self.logger.info("Attempting to scrape from equity list page...")

            # Fallback: Try scraping from the equity list page
            try:
                list_url = f"{self.base_url}/market-data/live-equity-market"
                response = self.fetch_page(list_url)

                if response:
                    soup = self.parse_html(response.text)
                    securities = self._scrape_securities_from_html(soup)

            except Exception as fallback_e:
                self.logger.error(f"Fallback scraping also failed: {fallback_e}")

        return securities

    def _parse_securities_data(self, data: Any) -> List[Dict[str, Any]]:
        """
        Parse securities data from various API response formats

        Args:
            data: API response data

        Returns:
            List of parsed securities
        """
        securities = []

        try:
            if isinstance(data, dict):
                # Try different keys where stock data might be
                for key in ['data', 'stocks', 'securities', 'records']:
                    if key in data:
                        stock_list = data[key]
                        if isinstance(stock_list, list):
                            for item in stock_list:
                                security = {
                                    'symbol': item.get('symbol', item.get('SYMBOL', '')),
                                    'company_name': item.get('companyName', item.get('NAME_OF_COMPANY', '')),
                                    'isin': item.get('isin', item.get('ISIN_NUMBER', '')),
                                    'last_price': item.get('lastPrice', item.get('LAST_TRADED_PRICE', 0)),
                                    'source': 'NSE',
                                    'scraped_at': datetime.now().isoformat()
                                }
                                securities.append(security)
                            break
            elif isinstance(data, list):
                # Data is already a list
                for item in data:
                    if isinstance(item, dict):
                        security = {
                            'symbol': item.get('symbol', item.get('SYMBOL', '')),
                            'company_name': item.get('companyName', item.get('NAME_OF_COMPANY', '')),
                            'isin': item.get('isin', item.get('ISIN_NUMBER', '')),
                            'last_price': item.get('lastPrice', item.get('LAST_TRADED_PRICE', 0)),
                            'source': 'NSE',
                            'scraped_at': datetime.now().isoformat()
                        }
                        securities.append(security)

        except Exception as e:
            self.logger.error(f"Error parsing securities data: {e}")

        return securities

    def _scrape_securities_from_html(self, soup) -> List[Dict[str, Any]]:
        """
        Scrape securities from HTML page as fallback

        Args:
            soup: BeautifulSoup object

        Returns:
            List of securities
        """
        securities = []

        try:
            # Look for tables containing security data
            tables = soup.find_all('table')

            for table in tables:
                rows = table.find_all('tr')

                # Try to identify header row
                headers = []
                for row in rows:
                    header_cells = row.find_all('th')
                    if header_cells:
                        headers = [cell.get_text(strip=True) for cell in header_cells]
                        break

                # Process data rows
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        security = {
                            'symbol': cells[0].get_text(strip=True) if len(cells) > 0 else '',
                            'company_name': cells[1].get_text(strip=True) if len(cells) > 1 else '',
                            'last_price': cells[2].get_text(strip=True) if len(cells) > 2 else '',
                            'source': 'NSE',
                            'scraped_at': datetime.now().isoformat()
                        }

                        if security['symbol']:  # Only add if symbol exists
                            securities.append(security)

            self.logger.info(f"Scraped {len(securities)} securities from HTML")

        except Exception as e:
            self.logger.error(f"Error scraping securities from HTML: {e}")

        return securities

    def get_all_nifty_indices(self) -> List[Dict[str, Any]]:
        """
        Get all NIFTY indices data

        Returns:
            List of index data dictionaries
        """
        self.logger.info("Fetching all NIFTY indices")

        indices = []

        try:
            # Get all indices data
            url = f"{self.base_url}/api/allIndices"
            response = self.fetch_page(url)

            if response:
                data = response.json()

                if isinstance(data, dict) and 'data' in data:
                    indices_data = data['data']
                elif isinstance(data, list):
                    indices_data = data
                else:
                    indices_data = []

                for idx in indices_data:
                    index_info = {
                        'index_name': idx.get('indexSymbol', idx.get('index', '')),
                        'last_price': idx.get('last', idx.get('lastPrice', 0)),
                        'change': idx.get('change', 0),
                        'pChange': idx.get('percentChange', idx.get('pChange', 0)),
                        'open': idx.get('open', 0),
                        'high': idx.get('high', 0),
                        'low': idx.get('low', 0),
                        'previous_close': idx.get('previousClose', 0),
                        'year_high': idx.get('yearHigh', 0),
                        'year_low': idx.get('yearLow', 0),
                        'source': 'NSE',
                        'scraped_at': datetime.now().isoformat()
                    }
                    indices.append(index_info)

                self.logger.info(f"Successfully fetched {len(indices)} indices")

        except Exception as e:
            self.logger.error(f"Error fetching NIFTY indices: {e}")

        return indices


if __name__ == "__main__":
    # Example usage
    scraper = NSEScraper()

    print("=" * 80)
    print("NSE Data Scraper - Demo")
    print("=" * 80)

    # Scrape equity securities
    print("\n1. Fetching equity securities/instruments...")
    securities = scraper.scrape_equity_securities()
    if securities:
        scraper.save_to_file(securities, 'nse_equity_securities.json', 'json')
        print(f"   ✓ Found {len(securities)} securities")
        print(f"   ✓ Sample: {securities[0] if securities else 'N/A'}")
    else:
        print("   ✗ No securities data retrieved")

    # Get all NIFTY indices
    print("\n2. Fetching NIFTY indices...")
    indices = scraper.get_all_nifty_indices()
    if indices:
        scraper.save_to_file(indices, 'nse_nifty_indices.json', 'json')
        print(f"   ✓ Found {len(indices)} indices")
        print(f"   ✓ Sample: {indices[0]['index_name'] if indices else 'N/A'}")
    else:
        print("   ✗ No indices data retrieved")

    # Scrape circulars
    print("\n3. Scraping circulars...")
    circulars = scraper.scrape_circulars(days=7)
    if circulars:
        scraper.save_to_file(circulars, 'nse_circulars.json', 'json')
        print(f"   ✓ Found {len(circulars)} circulars")
    else:
        print("   ✗ No circulars retrieved")

    # Scrape daily reports
    print("\n4. Scraping daily reports...")
    reports = scraper.scrape_daily_reports('equity')
    if reports:
        scraper.save_to_file(reports, 'nse_daily_reports.json', 'json')
        print(f"   ✓ Retrieved equity report")
    else:
        print("   ✗ No daily reports retrieved")

    # Scrape announcements
    print("\n5. Scraping announcements...")
    announcements = scraper.scrape_announcements()
    if announcements:
        scraper.save_to_file(announcements, 'nse_announcements.json', 'json')
        print(f"   ✓ Found {len(announcements)} announcements")
    else:
        print("   ✗ No announcements retrieved")

    print("\n" + "=" * 80)
    print("Scraping complete! Check the 'data' folder for output files.")
    print("=" * 80)
