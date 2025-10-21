"""
BSE (Bombay Stock Exchange) webscraper for circulars and daily reports
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import json
from base_scraper import BaseScraper
import config


class BSEScraper(BaseScraper):
    """Scraper for BSE India website"""

    def __init__(self):
        super().__init__("BSE_Scraper")
        self.base_url = config.BSE_BASE_URL

    def scrape_circulars(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Scrape circulars/announcements from BSE

        Args:
            days: Number of days to fetch circulars for (default: 7)

        Returns:
            List of circular dictionaries
        """
        self.logger.info(f"Scraping BSE circulars for the last {days} days")

        circulars = []

        # BSE Corporate Announcements URL
        url = config.BSE_CIRCULARS_URL

        try:
            response = self.fetch_page(url)
            if not response:
                self.logger.error("Failed to fetch BSE circulars")
                return circulars

            soup = self.parse_html(response.text)

            # Find announcement table
            tables = soup.find_all('table', {'class': ['tablesorter', 'data']})

            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        circular = {
                            'date': cols[0].get_text(strip=True) if len(cols) > 0 else '',
                            'company': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                            'category': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                            'subject': cols[3].get_text(strip=True) if len(cols) > 3 else '',
                            'attachment_link': self._extract_link(cols[4]) if len(cols) > 4 else '',
                            'source': 'BSE',
                            'scraped_at': datetime.now().isoformat()
                        }
                        circulars.append(circular)

            self.logger.info(f"Successfully scraped {len(circulars)} BSE circulars")

        except Exception as e:
            self.logger.error(f"Error scraping BSE circulars: {e}")

        return circulars

    def _extract_link(self, cell) -> str:
        """
        Extract link from table cell

        Args:
            cell: BeautifulSoup table cell element

        Returns:
            URL string or empty string
        """
        link = cell.find('a')
        if link and link.get('href'):
            href = link.get('href')
            if href.startswith('http'):
                return href
            else:
                return f"{self.base_url}/{href.lstrip('/')}"
        return ''

    def scrape_daily_reports(self, report_type: str = 'market_summary') -> List[Dict[str, Any]]:
        """
        Scrape daily reports from BSE

        Args:
            report_type: Type of report (market_summary, bhav_copy, etc.)

        Returns:
            List of report dictionaries
        """
        self.logger.info(f"Scraping BSE daily reports for {report_type}")

        reports = []

        # BSE Market Reports URL
        url = config.BSE_DAILY_REPORTS_URL

        try:
            response = self.fetch_page(url)
            if not response:
                self.logger.error(f"Failed to fetch BSE daily reports for {report_type}")
                return reports

            soup = self.parse_html(response.text)

            # Extract market summary data
            market_data = self._extract_market_data(soup)

            report = {
                'report_type': report_type,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'data': market_data,
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            }
            reports.append(report)

            self.logger.info(f"Successfully scraped BSE {report_type} report")

        except Exception as e:
            self.logger.error(f"Error scraping BSE daily reports: {e}")

        return reports

    def _extract_market_data(self, soup) -> Dict[str, Any]:
        """
        Extract market data from parsed HTML

        Args:
            soup: BeautifulSoup object

        Returns:
            Dictionary containing market data
        """
        market_data = {}

        try:
            # Find market statistics
            stats_divs = soup.find_all('div', class_=['market-stats', 'stats-box'])

            for div in stats_divs:
                label = div.find('span', class_='label')
                value = div.find('span', class_='value')

                if label and value:
                    market_data[label.get_text(strip=True)] = value.get_text(strip=True)

            # Find index values
            index_table = soup.find('table', {'id': 'indextable'})
            if index_table:
                market_data['indices'] = []
                rows = index_table.find_all('tr')[1:]
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        index_info = {
                            'name': cols[0].get_text(strip=True),
                            'value': cols[1].get_text(strip=True),
                            'change': cols[2].get_text(strip=True) if len(cols) > 2 else ''
                        }
                        market_data['indices'].append(index_info)

        except Exception as e:
            self.logger.warning(f"Error extracting market data: {e}")

        return market_data

    def scrape_bhavcopy(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Scrape BSE Bhavcopy (daily market report)

        Args:
            date: Date in format DDMMYY (e.g., 211023). If None, uses today's date

        Returns:
            Dictionary containing bhavcopy data
        """
        if date is None:
            date = datetime.now().strftime('%d%m%y')

        self.logger.info(f"Scraping BSE Bhavcopy for {date}")

        # BSE Bhavcopy URL format
        # Example: https://www.bseindia.com/download/BhavCopy/Equity/EQ211023_CSV.ZIP
        bhavcopy_url = f"{self.base_url}/download/BhavCopy/Equity/EQ{date}_CSV.ZIP"

        try:
            response = self.fetch_page(bhavcopy_url)
            if response:
                bhavcopy_data = {
                    'date': date,
                    'url': bhavcopy_url,
                    'content_length': len(response.content),
                    'source': 'BSE',
                    'scraped_at': datetime.now().isoformat()
                }

                # Save ZIP file
                filename = f"bse_bhavcopy_{date}.zip"
                output_path = config.DATA_DIR / filename

                with open(output_path, 'wb') as f:
                    f.write(response.content)

                self.logger.info(f"Successfully downloaded BSE Bhavcopy to {output_path}")
                return bhavcopy_data

        except Exception as e:
            self.logger.error(f"Error scraping BSE Bhavcopy: {e}")

        return {}

    def scrape_corporate_actions(self) -> List[Dict[str, Any]]:
        """
        Scrape corporate actions from BSE

        Returns:
            List of corporate action dictionaries
        """
        self.logger.info("Scraping BSE corporate actions")

        actions = []

        # BSE Corporate Actions URL
        url = f"{self.base_url}/corporates/corporate_act.aspx"

        try:
            response = self.fetch_page(url)
            if not response:
                return actions

            soup = self.parse_html(response.text)

            # Find corporate actions table
            tables = soup.find_all('table')

            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 5:
                        action = {
                            'company': cols[0].get_text(strip=True) if len(cols) > 0 else '',
                            'security_code': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                            'purpose': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                            'ex_date': cols[3].get_text(strip=True) if len(cols) > 3 else '',
                            'record_date': cols[4].get_text(strip=True) if len(cols) > 4 else '',
                            'source': 'BSE',
                            'scraped_at': datetime.now().isoformat()
                        }
                        actions.append(action)

            self.logger.info(f"Successfully scraped {len(actions)} BSE corporate actions")

        except Exception as e:
            self.logger.error(f"Error scraping BSE corporate actions: {e}")

        return actions

    def scrape_news(self, category: str = 'all') -> List[Dict[str, Any]]:
        """
        Scrape news from BSE

        Args:
            category: News category (all, market, corporate, etc.)

        Returns:
            List of news dictionaries
        """
        self.logger.info(f"Scraping BSE news for category: {category}")

        news_items = []

        # BSE News URL
        url = config.BSE_DAILY_REPORTS_URL

        try:
            response = self.fetch_page(url)
            if not response:
                return news_items

            soup = self.parse_html(response.text)

            # Find news sections
            news_divs = soup.find_all('div', class_=['news-item', 'market-news'])

            for div in news_divs:
                news = {
                    'title': div.find('h3').get_text(strip=True) if div.find('h3') else '',
                    'date': div.find('span', class_='date').get_text(strip=True) if div.find('span', class_='date') else '',
                    'category': category,
                    'content': div.get_text(strip=True),
                    'link': self._extract_link(div) if div.find('a') else '',
                    'source': 'BSE',
                    'scraped_at': datetime.now().isoformat()
                }
                news_items.append(news)

            self.logger.info(f"Successfully scraped {len(news_items)} BSE news items")

        except Exception as e:
            self.logger.error(f"Error scraping BSE news: {e}")

        return news_items


if __name__ == "__main__":
    # Example usage
    scraper = BSEScraper()

    # Scrape circulars
    circulars = scraper.scrape_circulars(days=7)
    if circulars:
        scraper.save_to_file(circulars, 'bse_circulars.json', 'json')

    # Scrape daily reports
    reports = scraper.scrape_daily_reports('market_summary')
    if reports:
        scraper.save_to_file(reports, 'bse_daily_reports.json', 'json')

    # Scrape corporate actions
    actions = scraper.scrape_corporate_actions()
    if actions:
        scraper.save_to_file(actions, 'bse_corporate_actions.json', 'json')

    # Scrape news
    news = scraper.scrape_news()
    if news:
        scraper.save_to_file(news, 'bse_news.json', 'json')
