# Deployment Guide - NSE/BSE Daily Newsletter System

This guide will help you deploy the automated newsletter system to run daily at 3:45 PM.

## Prerequisites

- Python 3.8 or higher
- Internet connection (for scraping and sending emails)
- Gmail account with App Password configured
- Server or local machine that can run 24/7

## Deployment Options

### Option 1: Local Machine (Simplest for Testing)

**Best for:** Running on your personal computer for testing or if you have a machine that runs 24/7.

#### Steps:

1. **Clone the repository to your local machine:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure email credentials:**
   ```bash
   cp .env.example .env
   nano .env  # or use any text editor
   ```

   Add your credentials:
   ```
   GMAIL_ADDRESS=benjamin.prajwal57@gmail.com
   GMAIL_APP_PASSWORD=auar pukc lfey oizs
   RECIPIENT_EMAIL=benjamin.prajwal57@gmail.com
   ```

4. **Test the newsletter:**
   ```bash
   python scheduler.py --now
   ```
   Check your email for the newsletter!

5. **Run the scheduler:**
   ```bash
   # Keep this terminal window open
   python scheduler.py
   ```

6. **Keep it running in background (recommended):**

   **Using screen:**
   ```bash
   screen -S newsletter
   python scheduler.py
   # Press Ctrl+A, then D to detach
   # To check: screen -r newsletter
   ```

   **Using nohup:**
   ```bash
   nohup python scheduler.py > newsletter.log 2>&1 &
   # Check logs: tail -f newsletter.log
   ```

---

### Option 2: Linux Server with systemd (Recommended for Production)

**Best for:** VPS, cloud servers, or dedicated Linux machines.

#### Steps:

1. **Set up on your server:**
   ```bash
   cd /home/your-username
   git clone <repository-url> nse-bse-newsletter
   cd nse-bse-newsletter
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure .env file** (same as Option 1, step 3)

4. **Create systemd service:**

   Use the provided service file:
   ```bash
   sudo cp newsletter-scheduler.service /etc/systemd/system/
   ```

   Edit the service file to match your setup:
   ```bash
   sudo nano /etc/systemd/system/newsletter-scheduler.service
   ```

   Update these lines:
   - `User=your-username`
   - `WorkingDirectory=/home/your-username/nse-bse-newsletter`
   - `ExecStart=/usr/bin/python3 /home/your-username/nse-bse-newsletter/scheduler.py`

5. **Enable and start the service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable newsletter-scheduler
   sudo systemctl start newsletter-scheduler
   ```

6. **Check status:**
   ```bash
   sudo systemctl status newsletter-scheduler
   ```

7. **View logs:**
   ```bash
   sudo journalctl -u newsletter-scheduler -f
   ```

---

### Option 3: Cloud Deployment (AWS EC2, DigitalOcean, etc.)

**Best for:** Production deployment with guaranteed uptime.

#### AWS EC2 Example:

1. **Launch an EC2 instance:**
   - Choose: Ubuntu 22.04 LTS (t2.micro is sufficient)
   - Configure security group (no special ports needed)
   - Download your key pair

2. **Connect to your instance:**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install Python and dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git -y
   ```

4. **Clone and set up:**
   ```bash
   git clone <repository-url> nse-bse-newsletter
   cd nse-bse-newsletter
   pip3 install -r requirements.txt
   ```

5. **Configure .env** (same as Option 1, step 3)

6. **Set up systemd service** (same as Option 2, steps 4-7)

#### DigitalOcean Droplet Example:

1. **Create a Droplet:**
   - Choose: Ubuntu 22.04
   - Plan: Basic ($6/month is sufficient)

2. **SSH into your droplet:**
   ```bash
   ssh root@your-droplet-ip
   ```

3. **Follow the same steps as AWS EC2** (steps 3-6)

---

### Option 4: Docker Deployment (Advanced)

**Best for:** Containerized deployments, Kubernetes, or Docker Compose setups.

A `Dockerfile` and `docker-compose.yml` can be created if needed. Let me know if you need this option!

---

## Monitoring and Maintenance

### Check if scheduler is running:

**Local (screen):**
```bash
screen -r newsletter
```

**systemd:**
```bash
sudo systemctl status newsletter-scheduler
```

**Process check:**
```bash
ps aux | grep scheduler.py
```

### View logs:

**Local:**
```bash
tail -f logs/scheduler.log
```

**systemd:**
```bash
sudo journalctl -u newsletter-scheduler -f
```

### Restart the scheduler:

**Local (screen):**
```bash
screen -r newsletter
# Press Ctrl+C to stop
python scheduler.py
```

**systemd:**
```bash
sudo systemctl restart newsletter-scheduler
```

### Stop the scheduler:

**Local (screen):**
```bash
screen -r newsletter
# Press Ctrl+C
```

**systemd:**
```bash
sudo systemctl stop newsletter-scheduler
```

---

## Troubleshooting

### Newsletter not being sent:

1. Check logs for errors:
   ```bash
   tail -50 logs/scheduler.log
   ```

2. Verify email credentials:
   ```bash
   cat .env
   ```

3. Test email sending:
   ```bash
   python scheduler.py --now
   ```

### Scraping errors (403 Forbidden):

- NSE/BSE websites have anti-scraping measures
- The scrapers may need enhancement with Selenium or proxy services
- Check the logs to see which specific endpoints are failing

### Scheduler not running at correct time:

1. Check system timezone:
   ```bash
   timedatectl
   ```

2. The scheduler runs at 3:45 PM (15:45) in your system's local timezone

3. To change the time, edit `scheduler.py`:
   ```python
   # Line ~145
   trigger=CronTrigger(hour=15, minute=45)  # Change these values
   ```

---

## Security Best Practices

1. **Protect your .env file:**
   ```bash
   chmod 600 .env
   ```

2. **Never commit .env to git:**
   - Already in `.gitignore`, but double-check!

3. **Use strong Gmail App Password:**
   - Already configured, keep it secure

4. **Regular updates:**
   ```bash
   cd nse-bse-newsletter
   git pull
   pip3 install -r requirements.txt --upgrade
   sudo systemctl restart newsletter-scheduler  # if using systemd
   ```

---

## Quick Reference

| Task | Command |
|------|---------|
| Start scheduler | `python scheduler.py` |
| Test newsletter | `python scheduler.py --now` |
| View logs | `tail -f logs/scheduler.log` |
| Check status | `sudo systemctl status newsletter-scheduler` |
| Restart service | `sudo systemctl restart newsletter-scheduler` |
| View demo | `python demo_newsletter.py` |

---

## Need Help?

- Check logs: `logs/scheduler.log`
- Test email: `python scheduler.py --now`
- View demo: `python demo_newsletter.py`

## Next Steps After Deployment

1. ✅ Test the newsletter: `python scheduler.py --now`
2. ✅ Check your email inbox
3. ✅ Verify the scheduler is running
4. ✅ Wait for 3:45 PM tomorrow to confirm automated sending
5. ✅ Monitor logs for the first few days

Good luck with your deployment! 🚀
