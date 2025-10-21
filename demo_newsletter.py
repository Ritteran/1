"""
Demo Newsletter Generator
Creates a sample newsletter with mock data to show what the email will look like
"""

from datetime import datetime, timedelta
from newsletter_formatter import NewsletterFormatter


def generate_mock_data():
    """Generate realistic mock data for demo purposes"""

    # Today and yesterday dates
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    mock_data = {
        'nse_circulars': [
            {
                'date': today,
                'company': 'Reliance Industries Limited',
                'symbol': 'RELIANCE',
                'subject': 'Board Meeting Intimation',
                'purpose': 'To consider and approve quarterly results for Q3 FY2025',
                'source': 'NSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'date': today,
                'company': 'Tata Consultancy Services',
                'symbol': 'TCS',
                'subject': 'Dividend Declaration',
                'purpose': 'Declaration of interim dividend of Rs 10 per share',
                'source': 'NSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'date': yesterday,
                'company': 'HDFC Bank Limited',
                'symbol': 'HDFCBANK',
                'subject': 'Acquisition Announcement',
                'purpose': 'Proposed acquisition of digital lending platform',
                'source': 'NSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'date': yesterday,
                'company': 'Infosys Limited',
                'symbol': 'INFY',
                'subject': 'Press Release',
                'purpose': 'Launch of new AI-powered solutions for enterprise clients',
                'source': 'NSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'date': today,
                'company': 'Bharti Airtel Limited',
                'symbol': 'BHARTIARTL',
                'subject': 'Rights Issue Announcement',
                'purpose': 'Rights issue to raise Rs 5,000 crores',
                'source': 'NSE',
                'scraped_at': datetime.now().isoformat()
            }
        ],

        'nse_announcements': [
            {
                'date': today,
                'company': 'ICICI Bank Limited',
                'symbol': 'ICICIBANK',
                'subject': 'Annual General Meeting Notice',
                'source': 'NSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'date': today,
                'company': 'State Bank of India',
                'symbol': 'SBIN',
                'subject': 'Disclosure under Regulation 30',
                'source': 'NSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'date': yesterday,
                'company': 'Wipro Limited',
                'symbol': 'WIPRO',
                'subject': 'Outcome of Board Meeting',
                'source': 'NSE',
                'scraped_at': datetime.now().isoformat()
            }
        ],

        'nse_daily_reports': [
            {
                'report_type': 'Market Summary',
                'nifty_50': '22,458.85',
                'change': '+245.30 (+1.10%)',
                'nifty_bank': '48,256.75',
                'bank_change': '+512.45 (+1.08%)',
                'volume': '₹65,234 crores',
                'advances': '1,245',
                'declines': '854',
                'source': 'NSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'report_type': 'Top Gainers',
                'stocks': 'TCS (+3.2%), RELIANCE (+2.8%), INFY (+2.5%)',
                'source': 'NSE',
                'scraped_at': datetime.now().isoformat()
            }
        ],

        'bse_circulars': [
            {
                'date': today,
                'company': 'Larsen & Toubro Limited',
                'category': 'Corporate Action',
                'subject': 'Bonus Issue - 1:2',
                'attachment_link': 'https://www.bseindia.com/...',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'date': today,
                'company': 'Mahindra & Mahindra Ltd',
                'category': 'Announcement',
                'subject': 'Launch of new EV platform',
                'attachment_link': 'https://www.bseindia.com/...',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'date': yesterday,
                'company': 'Bajaj Finance Limited',
                'category': 'Results',
                'subject': 'Q3 FY25 Financial Results',
                'attachment_link': 'https://www.bseindia.com/...',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'date': yesterday,
                'company': 'Asian Paints Limited',
                'category': 'Corporate Action',
                'subject': 'Record Date for Dividend',
                'attachment_link': 'https://www.bseindia.com/...',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            }
        ],

        'bse_corporate_actions': [
            {
                'company': 'ITC Limited',
                'symbol': 'ITC',
                'purpose': 'Dividend - Rs 6.75 per share',
                'ex_date': '2025-10-25',
                'record_date': '2025-10-26',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'company': 'Hindustan Unilever Ltd',
                'symbol': 'HINDUNILVR',
                'purpose': 'Interim Dividend - Rs 19 per share',
                'ex_date': '2025-10-28',
                'record_date': '2025-10-29',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'company': 'Adani Ports and SEZ',
                'symbol': 'ADANIPORTS',
                'purpose': 'Stock Split - Face value Rs 2 to Rs 1',
                'ex_date': '2025-11-01',
                'record_date': '2025-11-02',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'company': 'Sun Pharmaceutical',
                'symbol': 'SUNPHARMA',
                'purpose': 'Bonus Issue - 1:1',
                'ex_date': '2025-11-05',
                'record_date': '2025-11-06',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'company': 'Kotak Mahindra Bank',
                'symbol': 'KOTAKBANK',
                'purpose': 'Dividend - Rs 2.50 per share',
                'ex_date': '2025-10-30',
                'record_date': '2025-10-31',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            }
        ],

        'bse_news': [
            {
                'title': 'BSE SENSEX closes above 74,000 mark for first time',
                'date': today,
                'category': 'Market Update',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Foreign Institutional Investors net buyers at Rs 3,245 crores',
                'date': today,
                'category': 'FII/DII Activity',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'India VIX falls 5.2% indicating lower market volatility',
                'date': today,
                'category': 'Market Indicators',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'BSE launches new derivatives contracts on banking stocks',
                'date': yesterday,
                'category': 'Exchange News',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Record trading volumes in mid-cap and small-cap segments',
                'date': yesterday,
                'category': 'Market Activity',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            }
        ],

        'bse_daily_reports': [
            {
                'report_type': 'SENSEX Summary',
                'sensex': '74,125.35',
                'change': '+658.45 (+0.90%)',
                'bse_500': '32,456.20',
                'bse_500_change': '+325.15 (+1.01%)',
                'market_cap': '₹425.6 lakh crores',
                'turnover': '₹8,542 crores',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'report_type': 'Sectoral Performance',
                'best_sector': 'IT (+2.5%)',
                'worst_sector': 'PSU Banks (-0.8%)',
                'source': 'BSE',
                'scraped_at': datetime.now().isoformat()
            }
        ]
    }

    return mock_data


def main():
    """Generate and display demo newsletter"""
    print("\n" + "="*80)
    print("DEMO NEWSLETTER GENERATION")
    print("="*80 + "\n")

    print("Generating mock market data...")
    mock_data = generate_mock_data()

    print("Creating newsletter formatter...")
    formatter = NewsletterFormatter()

    print("Formatting newsletter...\n")
    newsletter = formatter.generate_newsletter(mock_data)

    print("="*80)
    print("PREVIEW OF EMAIL THAT WILL BE SENT TO: benjamin.prajwal57@gmail.com")
    print("="*80)
    print("\nSUBJECT: NSE/BSE Daily Market Newsletter - " + datetime.now().strftime('%B %d, %Y'))
    print("\n" + "="*80)
    print(newsletter)
    print("="*80 + "\n")

    print("\nNewsletter Length: {} characters".format(len(newsletter)))
    print("This newsletter will be sent as plain text email.\n")


if __name__ == "__main__":
    main()
