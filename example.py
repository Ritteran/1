#!/usr/bin/env python3
"""
Example script demonstrating how to use NSE and BSE scrapers
"""

from nse_scraper import NSEScraper
from bse_scraper import BSEScraper
import json


def example_nse():
    """Example: Using NSE scraper"""
    print("=" * 60)
    print("NSE Scraper Example")
    print("=" * 60)

    # Initialize NSE scraper
    nse = NSEScraper()

    # Example 1: Scrape circulars
    print("\n1. Scraping NSE circulars...")
    circulars = nse.scrape_circulars(days=7)
    if circulars:
        print(f"   Found {len(circulars)} circulars")
        print(f"   Sample: {json.dumps(circulars[0], indent=2)[:200]}...")
        nse.save_to_file(circulars, 'example_nse_circulars.json', 'json')

    # Example 2: Scrape daily reports
    print("\n2. Scraping NSE daily reports...")
    reports = nse.scrape_daily_reports('equity')
    if reports:
        print(f"   Found {len(reports)} reports")
        nse.save_to_file(reports, 'example_nse_reports.json', 'json')

    # Example 3: Scrape announcements
    print("\n3. Scraping NSE announcements...")
    announcements = nse.scrape_announcements()
    if announcements:
        print(f"   Found {len(announcements)} announcements")
        nse.save_to_file(announcements, 'example_nse_announcements.json', 'json')

    print("\n" + "=" * 60)


def example_bse():
    """Example: Using BSE scraper"""
    print("=" * 60)
    print("BSE Scraper Example")
    print("=" * 60)

    # Initialize BSE scraper
    bse = BSEScraper()

    # Example 1: Scrape circulars
    print("\n1. Scraping BSE circulars...")
    circulars = bse.scrape_circulars(days=7)
    if circulars:
        print(f"   Found {len(circulars)} circulars")
        print(f"   Sample: {json.dumps(circulars[0], indent=2)[:200]}...")
        bse.save_to_file(circulars, 'example_bse_circulars.json', 'json')

    # Example 2: Scrape daily reports
    print("\n2. Scraping BSE daily reports...")
    reports = bse.scrape_daily_reports('market_summary')
    if reports:
        print(f"   Found {len(reports)} reports")
        bse.save_to_file(reports, 'example_bse_reports.json', 'json')

    # Example 3: Scrape corporate actions
    print("\n3. Scraping BSE corporate actions...")
    actions = bse.scrape_corporate_actions()
    if actions:
        print(f"   Found {len(actions)} corporate actions")
        bse.save_to_file(actions, 'example_bse_actions.json', 'json')

    # Example 4: Scrape news
    print("\n4. Scraping BSE news...")
    news = bse.scrape_news()
    if news:
        print(f"   Found {len(news)} news items")
        bse.save_to_file(news, 'example_bse_news.json', 'json')

    print("\n" + "=" * 60)


def custom_example():
    """Example: Custom usage with data processing"""
    print("=" * 60)
    print("Custom Data Processing Example")
    print("=" * 60)

    nse = NSEScraper()

    # Scrape and process data
    print("\nFetching NSE circulars...")
    circulars = nse.scrape_circulars(days=30)

    if circulars:
        # Filter circulars by company
        target_companies = ['RELIANCE', 'TCS', 'INFY', 'HDFC']
        filtered = [c for c in circulars if any(company in c.get('symbol', '') for company in target_companies)]

        print(f"\nTotal circulars: {len(circulars)}")
        print(f"Filtered circulars for target companies: {len(filtered)}")

        if filtered:
            print("\nSample filtered circular:")
            print(json.dumps(filtered[0], indent=2))

            # Save filtered data
            nse.save_to_file(filtered, 'filtered_circulars.json', 'json')
            print("\nFiltered data saved to data/filtered_circulars.json")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("# NSE/BSE Scraper Examples")
    print("#" * 60 + "\n")

    # Run examples
    try:
        example_nse()
    except Exception as e:
        print(f"\nNSE Example Error: {e}")

    print("\n")

    try:
        example_bse()
    except Exception as e:
        print(f"\nBSE Example Error: {e}")

    print("\n")

    try:
        custom_example()
    except Exception as e:
        print(f"\nCustom Example Error: {e}")

    print("\n" + "#" * 60)
    print("# Examples completed!")
    print("# Check the 'data' directory for output files")
    print("#" * 60 + "\n")
