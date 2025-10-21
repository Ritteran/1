#!/usr/bin/env python3
"""
Main script to run NSE and BSE webscrapers
"""

import argparse
import sys
from datetime import datetime
from nse_scraper import NSEScraper
from bse_scraper import BSEScraper


def scrape_nse(args):
    """Run NSE scraper based on arguments"""
    scraper = NSEScraper()

    print(f"\n{'='*60}")
    print(f"NSE Scraper - Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    results = {}

    if args.circulars:
        print(f"Fetching NSE circulars for the last {args.days} days...")
        circulars = scraper.scrape_circulars(days=args.days)
        if circulars:
            scraper.save_to_file(circulars, 'nse_circulars.json', 'json')
            scraper.save_to_file(circulars, 'nse_circulars.csv', 'csv')
            results['circulars'] = len(circulars)
            print(f"✓ Scraped {len(circulars)} circulars")
        else:
            print("✗ No circulars found")

    if args.reports:
        print(f"\nFetching NSE daily reports...")
        reports = scraper.scrape_daily_reports('equity')
        if reports:
            scraper.save_to_file(reports, 'nse_daily_reports.json', 'json')
            results['reports'] = len(reports)
            print(f"✓ Scraped {len(reports)} reports")
        else:
            print("✗ No reports found")

    if args.announcements:
        print(f"\nFetching NSE announcements...")
        announcements = scraper.scrape_announcements()
        if announcements:
            scraper.save_to_file(announcements, 'nse_announcements.json', 'json')
            results['announcements'] = len(announcements)
            print(f"✓ Scraped {len(announcements)} announcements")
        else:
            print("✗ No announcements found")

    if args.bhavcopy:
        print(f"\nFetching NSE Bhavcopy...")
        bhavcopy = scraper.scrape_equity_bhavcopy()
        if bhavcopy:
            results['bhavcopy'] = 1
            print(f"✓ Downloaded Bhavcopy")
        else:
            print("✗ Failed to download Bhavcopy")

    print(f"\n{'='*60}")
    print(f"NSE Scraper - Completed")
    print(f"{'='*60}\n")

    return results


def scrape_bse(args):
    """Run BSE scraper based on arguments"""
    scraper = BSEScraper()

    print(f"\n{'='*60}")
    print(f"BSE Scraper - Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    results = {}

    if args.circulars:
        print(f"Fetching BSE circulars for the last {args.days} days...")
        circulars = scraper.scrape_circulars(days=args.days)
        if circulars:
            scraper.save_to_file(circulars, 'bse_circulars.json', 'json')
            scraper.save_to_file(circulars, 'bse_circulars.csv', 'csv')
            results['circulars'] = len(circulars)
            print(f"✓ Scraped {len(circulars)} circulars")
        else:
            print("✗ No circulars found")

    if args.reports:
        print(f"\nFetching BSE daily reports...")
        reports = scraper.scrape_daily_reports('market_summary')
        if reports:
            scraper.save_to_file(reports, 'bse_daily_reports.json', 'json')
            results['reports'] = len(reports)
            print(f"✓ Scraped {len(reports)} reports")
        else:
            print("✗ No reports found")

    if args.corporate_actions:
        print(f"\nFetching BSE corporate actions...")
        actions = scraper.scrape_corporate_actions()
        if actions:
            scraper.save_to_file(actions, 'bse_corporate_actions.json', 'json')
            scraper.save_to_file(actions, 'bse_corporate_actions.csv', 'csv')
            results['corporate_actions'] = len(actions)
            print(f"✓ Scraped {len(actions)} corporate actions")
        else:
            print("✗ No corporate actions found")

    if args.news:
        print(f"\nFetching BSE news...")
        news = scraper.scrape_news()
        if news:
            scraper.save_to_file(news, 'bse_news.json', 'json')
            results['news'] = len(news)
            print(f"✓ Scraped {len(news)} news items")
        else:
            print("✗ No news found")

    if args.bhavcopy:
        print(f"\nFetching BSE Bhavcopy...")
        bhavcopy = scraper.scrape_bhavcopy()
        if bhavcopy:
            results['bhavcopy'] = 1
            print(f"✓ Downloaded Bhavcopy")
        else:
            print("✗ Failed to download Bhavcopy")

    print(f"\n{'='*60}")
    print(f"BSE Scraper - Completed")
    print(f"{'='*60}\n")

    return results


def main():
    """Main function to parse arguments and run scrapers"""
    parser = argparse.ArgumentParser(
        description='NSE and BSE Webscraper for Circulars and Daily Reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape NSE circulars and reports
  python main.py --exchange nse --circulars --reports

  # Scrape BSE circulars for the last 30 days
  python main.py --exchange bse --circulars --days 30

  # Scrape everything from both exchanges
  python main.py --exchange both --all

  # Scrape specific items
  python main.py --exchange nse --circulars --announcements --bhavcopy
        """
    )

    parser.add_argument(
        '--exchange',
        choices=['nse', 'bse', 'both'],
        default='both',
        help='Exchange to scrape (default: both)'
    )

    parser.add_argument(
        '--circulars',
        action='store_true',
        help='Scrape circulars/announcements'
    )

    parser.add_argument(
        '--reports',
        action='store_true',
        help='Scrape daily reports'
    )

    parser.add_argument(
        '--announcements',
        action='store_true',
        help='Scrape announcements (NSE only)'
    )

    parser.add_argument(
        '--corporate-actions',
        action='store_true',
        help='Scrape corporate actions (BSE only)'
    )

    parser.add_argument(
        '--news',
        action='store_true',
        help='Scrape news (BSE only)'
    )

    parser.add_argument(
        '--bhavcopy',
        action='store_true',
        help='Download Bhavcopy (daily market report)'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Scrape all available data'
    )

    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to fetch data for (default: 7)'
    )

    args = parser.parse_args()

    # If --all is specified, enable all scrapers
    if args.all:
        args.circulars = True
        args.reports = True
        args.announcements = True
        args.corporate_actions = True
        args.news = True
        args.bhavcopy = True

    # If no specific scraper is selected, show help
    if not any([args.circulars, args.reports, args.announcements,
                args.corporate_actions, args.news, args.bhavcopy]):
        parser.print_help()
        sys.exit(1)

    print(f"\n{'#'*60}")
    print(f"# NSE/BSE Webscraper")
    print(f"# Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*60}")

    # Run scrapers based on exchange selection
    if args.exchange in ['nse', 'both']:
        scrape_nse(args)

    if args.exchange in ['bse', 'both']:
        scrape_bse(args)

    print(f"\n{'#'*60}")
    print(f"# All scraping tasks completed!")
    print(f"# Check the 'data' directory for output files")
    print(f"{'#'*60}\n")


if __name__ == "__main__":
    main()
