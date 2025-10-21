"""
Newsletter Formatter Module
Generates plain text summaries of scraped NSE/BSE data
"""

from datetime import datetime
from typing import List, Dict, Any


class NewsletterFormatter:
    """Formats scraped data into plain text newsletter"""

    def __init__(self):
        self.width = 80  # Character width for formatting

    def _create_separator(self, char='='):
        """Create a separator line"""
        return char * self.width

    def _create_header(self, title):
        """Create a formatted header"""
        return f"\n{self._create_separator()}\n{title.center(self.width)}\n{self._create_separator()}\n"

    def _create_section(self, title):
        """Create a section header"""
        return f"\n{title}\n{'-' * len(title)}\n"

    def _format_circulars(self, circulars: List[Dict[str, Any]], source: str):
        """Format circulars data"""
        if not circulars:
            return f"\nNo {source} circulars found.\n"

        output = self._create_section(f"{source} CIRCULARS ({len(circulars)} items)")

        for i, circular in enumerate(circulars[:10], 1):  # Limit to 10 most recent
            output += f"\n{i}. {circular.get('company', 'N/A')} ({circular.get('symbol', 'N/A')})\n"
            output += f"   Date: {circular.get('date', 'N/A')}\n"
            output += f"   Subject: {circular.get('subject', 'N/A')}\n"

            # Add category for BSE
            if 'category' in circular:
                output += f"   Category: {circular.get('category', 'N/A')}\n"

            # Add purpose for NSE
            if 'purpose' in circular:
                output += f"   Purpose: {circular.get('purpose', 'N/A')}\n"

        if len(circulars) > 10:
            output += f"\n... and {len(circulars) - 10} more circulars.\n"

        return output

    def _format_daily_reports(self, reports: List[Dict[str, Any]], source: str):
        """Format daily reports data"""
        if not reports:
            return f"\nNo {source} daily reports found.\n"

        output = self._create_section(f"{source} DAILY REPORTS ({len(reports)} items)")

        for i, report in enumerate(reports[:5], 1):  # Limit to 5 most recent
            output += f"\n{i}. Report Type: {report.get('report_type', 'N/A')}\n"

            # Show key metrics if available
            for key, value in report.items():
                if key not in ['report_type', 'source', 'scraped_at']:
                    output += f"   {key}: {value}\n"

        if len(reports) > 5:
            output += f"\n... and {len(reports) - 5} more reports.\n"

        return output

    def _format_announcements(self, announcements: List[Dict[str, Any]]):
        """Format NSE announcements"""
        if not announcements:
            return "\nNo NSE announcements found.\n"

        output = self._create_section(f"NSE ANNOUNCEMENTS ({len(announcements)} items)")

        for i, announcement in enumerate(announcements[:10], 1):
            output += f"\n{i}. {announcement.get('company', 'N/A')} ({announcement.get('symbol', 'N/A')})\n"
            output += f"   Date: {announcement.get('date', 'N/A')}\n"
            output += f"   Subject: {announcement.get('subject', 'N/A')}\n"

        if len(announcements) > 10:
            output += f"\n... and {len(announcements) - 10} more announcements.\n"

        return output

    def _format_corporate_actions(self, actions: List[Dict[str, Any]]):
        """Format BSE corporate actions"""
        if not actions:
            return "\nNo BSE corporate actions found.\n"

        output = self._create_section(f"BSE CORPORATE ACTIONS ({len(actions)} items)")

        for i, action in enumerate(actions[:10], 1):
            output += f"\n{i}. {action.get('company', 'N/A')} ({action.get('symbol', 'N/A')})\n"
            output += f"   Action: {action.get('purpose', 'N/A')}\n"
            output += f"   Ex-Date: {action.get('ex_date', 'N/A')}\n"
            output += f"   Record Date: {action.get('record_date', 'N/A')}\n"

        if len(actions) > 10:
            output += f"\n... and {len(actions) - 10} more corporate actions.\n"

        return output

    def _format_news(self, news: List[Dict[str, Any]]):
        """Format BSE news"""
        if not news:
            return "\nNo BSE news found.\n"

        output = self._create_section(f"BSE NEWS ({len(news)} items)")

        for i, item in enumerate(news[:10], 1):
            output += f"\n{i}. {item.get('title', 'N/A')}\n"
            output += f"   Date: {item.get('date', 'N/A')}\n"
            if 'category' in item:
                output += f"   Category: {item.get('category', 'N/A')}\n"

        if len(news) > 10:
            output += f"\n... and {len(news) - 10} more news items.\n"

        return output

    def _create_summary_stats(self, data_counts: Dict[str, int]):
        """Create summary statistics section"""
        output = self._create_section("SUMMARY STATISTICS")

        total_items = sum(data_counts.values())
        output += f"\nTotal Items Collected: {total_items}\n\n"

        for category, count in data_counts.items():
            output += f"  - {category}: {count}\n"

        return output

    def generate_newsletter(self, scraped_data: Dict[str, Any]):
        """
        Generate complete newsletter from scraped data

        Args:
            scraped_data (dict): Dictionary containing all scraped data with keys:
                - nse_circulars
                - bse_circulars
                - nse_daily_reports
                - bse_daily_reports
                - nse_announcements
                - bse_corporate_actions
                - bse_news

        Returns:
            str: Formatted plain text newsletter
        """
        # Create newsletter header
        newsletter = self._create_header("NSE/BSE DAILY MARKET NEWSLETTER")
        newsletter += f"\nGenerated: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}\n"

        # Calculate statistics
        data_counts = {
            "NSE Circulars": len(scraped_data.get('nse_circulars', [])),
            "BSE Circulars": len(scraped_data.get('bse_circulars', [])),
            "NSE Daily Reports": len(scraped_data.get('nse_daily_reports', [])),
            "BSE Daily Reports": len(scraped_data.get('bse_daily_reports', [])),
            "NSE Announcements": len(scraped_data.get('nse_announcements', [])),
            "BSE Corporate Actions": len(scraped_data.get('bse_corporate_actions', [])),
            "BSE News": len(scraped_data.get('bse_news', []))
        }

        # Add summary
        newsletter += self._create_summary_stats(data_counts)

        # Add NSE sections
        newsletter += self._create_header("NSE (National Stock Exchange)")
        newsletter += self._format_circulars(
            scraped_data.get('nse_circulars', []), 'NSE'
        )
        newsletter += self._format_announcements(
            scraped_data.get('nse_announcements', [])
        )
        newsletter += self._format_daily_reports(
            scraped_data.get('nse_daily_reports', []), 'NSE'
        )

        # Add BSE sections
        newsletter += self._create_header("BSE (Bombay Stock Exchange)")
        newsletter += self._format_circulars(
            scraped_data.get('bse_circulars', []), 'BSE'
        )
        newsletter += self._format_corporate_actions(
            scraped_data.get('bse_corporate_actions', [])
        )
        newsletter += self._format_news(
            scraped_data.get('bse_news', [])
        )
        newsletter += self._format_daily_reports(
            scraped_data.get('bse_daily_reports', []), 'BSE'
        )

        # Add footer
        newsletter += self._create_separator()
        newsletter += "\nEnd of Daily Newsletter\n"
        newsletter += f"Data saved in: /home/user/1/data/\n"
        newsletter += self._create_separator()

        return newsletter


if __name__ == "__main__":
    # Test the formatter
    test_data = {
        'nse_circulars': [
            {
                'date': '2025-10-21',
                'company': 'Reliance Industries',
                'symbol': 'RELIANCE',
                'subject': 'Board Meeting Notice',
                'purpose': 'Q3 Results'
            }
        ],
        'bse_circulars': [],
        'nse_announcements': [],
        'nse_daily_reports': [],
        'bse_corporate_actions': [],
        'bse_news': [],
        'bse_daily_reports': []
    }

    formatter = NewsletterFormatter()
    newsletter = formatter.generate_newsletter(test_data)
    print(newsletter)
