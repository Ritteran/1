"""
Daily Scheduler for NSE/BSE Scraper
Runs daily at 3:45 PM and sends newsletter via email
"""

import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import os
import sys

from nse_scraper import NSEScraper
from bse_scraper import BSEScraper
from newsletter_formatter import NewsletterFormatter
from email_sender import EmailSender


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class DailyNewsletterScheduler:
    """Manages daily scraping and newsletter sending"""

    def __init__(self):
        """Initialize scrapers and email sender"""
        self.nse_scraper = NSEScraper()
        self.bse_scraper = BSEScraper()
        self.formatter = NewsletterFormatter()
        self.email_sender = EmailSender()
        self.scheduler = BlockingScheduler()

        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)

    def run_daily_scrape(self):
        """
        Execute daily scraping routine and send newsletter
        This is the main task that runs on schedule
        """
        logger.info("=" * 80)
        logger.info("Starting scheduled scraping task")
        logger.info("=" * 80)

        try:
            scraped_data = self._scrape_all_data()
            newsletter_body = self._format_newsletter(scraped_data)
            success = self._send_newsletter(newsletter_body)

            if success:
                logger.info("Daily newsletter task completed successfully")
            else:
                logger.error("Failed to send newsletter email")

        except Exception as e:
            logger.error(f"Error in daily scrape task: {e}", exc_info=True)
            # Try to send error notification
            try:
                self.email_sender.send_error_notification(str(e))
            except Exception as email_error:
                logger.error(f"Failed to send error notification: {email_error}")

    def _scrape_all_data(self):
        """
        Scrape all available data from NSE and BSE

        Returns:
            dict: Dictionary containing all scraped data
        """
        logger.info("Starting data scraping...")

        scraped_data = {
            'nse_circulars': [],
            'nse_announcements': [],
            'nse_daily_reports': [],
            'bse_circulars': [],
            'bse_corporate_actions': [],
            'bse_news': [],
            'bse_daily_reports': []
        }

        # Scrape NSE data
        logger.info("Scraping NSE circulars...")
        try:
            scraped_data['nse_circulars'] = self.nse_scraper.scrape_circulars(days=1)
            logger.info(f"Found {len(scraped_data['nse_circulars'])} NSE circulars")
        except Exception as e:
            logger.error(f"Error scraping NSE circulars: {e}")

        logger.info("Scraping NSE announcements...")
        try:
            scraped_data['nse_announcements'] = self.nse_scraper.scrape_announcements()
            logger.info(f"Found {len(scraped_data['nse_announcements'])} NSE announcements")
        except Exception as e:
            logger.error(f"Error scraping NSE announcements: {e}")

        logger.info("Scraping NSE daily reports...")
        try:
            scraped_data['nse_daily_reports'] = self.nse_scraper.scrape_daily_reports()
            logger.info(f"Found {len(scraped_data['nse_daily_reports'])} NSE daily reports")
        except Exception as e:
            logger.error(f"Error scraping NSE daily reports: {e}")

        # Scrape BSE data
        logger.info("Scraping BSE circulars...")
        try:
            scraped_data['bse_circulars'] = self.bse_scraper.scrape_circulars(days=1)
            logger.info(f"Found {len(scraped_data['bse_circulars'])} BSE circulars")
        except Exception as e:
            logger.error(f"Error scraping BSE circulars: {e}")

        logger.info("Scraping BSE corporate actions...")
        try:
            scraped_data['bse_corporate_actions'] = self.bse_scraper.scrape_corporate_actions()
            logger.info(f"Found {len(scraped_data['bse_corporate_actions'])} BSE corporate actions")
        except Exception as e:
            logger.error(f"Error scraping BSE corporate actions: {e}")

        logger.info("Scraping BSE news...")
        try:
            scraped_data['bse_news'] = self.bse_scraper.scrape_news()
            logger.info(f"Found {len(scraped_data['bse_news'])} BSE news items")
        except Exception as e:
            logger.error(f"Error scraping BSE news: {e}")

        logger.info("Scraping BSE daily reports...")
        try:
            scraped_data['bse_daily_reports'] = self.bse_scraper.scrape_daily_reports()
            logger.info(f"Found {len(scraped_data['bse_daily_reports'])} BSE daily reports")
        except Exception as e:
            logger.error(f"Error scraping BSE daily reports: {e}")

        # Save all data to files
        logger.info("Saving scraped data to files...")
        self._save_data(scraped_data)

        return scraped_data

    def _save_data(self, scraped_data):
        """Save scraped data to JSON files"""
        try:
            # Save NSE data
            if scraped_data['nse_circulars']:
                self.nse_scraper.save_to_file(
                    scraped_data['nse_circulars'], 'nse_circulars.json', 'json'
                )

            if scraped_data['nse_announcements']:
                self.nse_scraper.save_to_file(
                    scraped_data['nse_announcements'], 'nse_announcements.json', 'json'
                )

            if scraped_data['nse_daily_reports']:
                self.nse_scraper.save_to_file(
                    scraped_data['nse_daily_reports'], 'nse_daily_reports.json', 'json'
                )

            # Save BSE data
            if scraped_data['bse_circulars']:
                self.bse_scraper.save_to_file(
                    scraped_data['bse_circulars'], 'bse_circulars.json', 'json'
                )

            if scraped_data['bse_corporate_actions']:
                self.bse_scraper.save_to_file(
                    scraped_data['bse_corporate_actions'], 'bse_corporate_actions.json', 'json'
                )

            if scraped_data['bse_news']:
                self.bse_scraper.save_to_file(
                    scraped_data['bse_news'], 'bse_news.json', 'json'
                )

            if scraped_data['bse_daily_reports']:
                self.bse_scraper.save_to_file(
                    scraped_data['bse_daily_reports'], 'bse_daily_reports.json', 'json'
                )

            logger.info("All data saved successfully")

        except Exception as e:
            logger.error(f"Error saving data: {e}")

    def _format_newsletter(self, scraped_data):
        """
        Format scraped data into newsletter

        Args:
            scraped_data (dict): All scraped data

        Returns:
            str: Formatted newsletter text
        """
        logger.info("Formatting newsletter...")
        newsletter = self.formatter.generate_newsletter(scraped_data)
        logger.info("Newsletter formatted successfully")
        return newsletter

    def _send_newsletter(self, newsletter_body):
        """
        Send newsletter via email

        Args:
            newsletter_body (str): Newsletter content

        Returns:
            bool: True if sent successfully
        """
        subject = f"NSE/BSE Daily Market Newsletter - {datetime.now().strftime('%B %d, %Y')}"
        logger.info(f"Sending newsletter: {subject}")

        success = self.email_sender.send_newsletter(subject, newsletter_body)

        if success:
            logger.info("Newsletter sent successfully")
        else:
            logger.error("Failed to send newsletter")

        return success

    def start(self):
        """
        Start the scheduler
        Runs daily at 3:45 PM
        """
        logger.info("Initializing scheduler...")

        # Schedule daily task at 3:45 PM
        self.scheduler.add_job(
            self.run_daily_scrape,
            trigger=CronTrigger(hour=15, minute=45),  # 3:45 PM
            id='daily_newsletter',
            name='Daily NSE/BSE Newsletter',
            replace_existing=True
        )

        logger.info("=" * 80)
        logger.info("Scheduler started successfully!")
        logger.info("Daily newsletter will run at 3:45 PM every day")
        logger.info("Press Ctrl+C to exit")
        logger.info("=" * 80)

        # List scheduled jobs
        jobs = self.scheduler.get_jobs()
        for job in jobs:
            logger.info(f"Scheduled: {job.name} - Next run: {job.next_run_time}")

        # Start scheduler (blocking)
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler stopped by user")
            self.scheduler.shutdown()

    def run_now(self):
        """Run the scraping task immediately (for testing)"""
        logger.info("Running scraping task immediately (test mode)")
        self.run_daily_scrape()


def main():
    """Main entry point"""
    scheduler = DailyNewsletterScheduler()

    # Check if running in test mode
    if len(sys.argv) > 1 and sys.argv[1] == '--now':
        scheduler.run_now()
    else:
        scheduler.start()


if __name__ == "__main__":
    main()
