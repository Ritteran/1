# Quick Start Guide

Get the newsletter system running in 5 minutes!

## Prerequisites

- ✅ Gmail App Password configured (you already have: `auar pukc lfey oizs`)
- ✅ Python 3.8+ installed
- ✅ Internet connection

## Super Quick Deployment (Automated)

```bash
# 1. Run the deployment script
./deploy.sh

# 2. Choose option 4 to test
# This will send a test email immediately

# 3. Run again and choose option 2 for background mode
./deploy.sh
```

That's it! The newsletter will now run daily at 3:45 PM.

## Manual Deployment (3 Steps)

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Your .env is already configured with:
#    GMAIL_ADDRESS=benjamin.prajwal57@gmail.com
#    GMAIL_APP_PASSWORD=auar pukc lfey oizs
#    RECIPIENT_EMAIL=benjamin.prajwal57@gmail.com

# 3. Start the scheduler
python3 scheduler.py
```

## Test It Now

```bash
# Send a test newsletter immediately
python3 scheduler.py --now

# Check your email at: benjamin.prajwal57@gmail.com
```

## View Demo Newsletter

```bash
# See what the newsletter looks like
python3 demo_newsletter.py
```

## Keep It Running 24/7

**Option 1: Using screen (simplest)**
```bash
screen -S newsletter
python3 scheduler.py
# Press Ctrl+A, then D to detach
```

**Option 2: Using systemd (recommended for servers)**
```bash
./deploy.sh
# Choose option 3
```

## Check Status

```bash
# View logs
tail -f logs/scheduler.log

# If using screen
screen -r newsletter

# If using systemd
sudo systemctl status newsletter-scheduler
```

## Deployment Locations

You can deploy this on:

- ✅ **Your local machine** - if it runs 24/7
- ✅ **AWS EC2** - t2.micro free tier is enough
- ✅ **DigitalOcean** - $6/month droplet
- ✅ **Google Cloud** - free tier
- ✅ **Any VPS** - with Python and internet

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Schedule

- **Runs daily at:** 3:45 PM (15:45)
- **Sends email to:** benjamin.prajwal57@gmail.com
- **Saves data to:** `data/` directory
- **Logs to:** `logs/scheduler.log`

## What You'll Receive

Every day at 3:45 PM, you'll get an email with:

- NSE Circulars & Announcements
- BSE Circulars & Corporate Actions
- Market summaries (NIFTY, SENSEX)
- Corporate actions (dividends, bonuses, splits)
- Latest market news

## Troubleshooting

**Problem:** Email not received
```bash
# Check logs
tail -20 logs/scheduler.log

# Test email
python3 scheduler.py --now
```

**Problem:** Scheduler not running
```bash
# Check if process is running
ps aux | grep scheduler.py

# Restart
./deploy.sh
```

**Problem:** Scraping errors (403)
- This is normal - NSE/BSE have anti-scraping measures
- The system handles errors gracefully
- You'll still get a newsletter with whatever data was successfully scraped

## Need More Help?

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment guide.

---

**Ready to go!** Just run `./deploy.sh` and choose your deployment method. 🚀
