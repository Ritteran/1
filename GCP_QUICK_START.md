# Google Cloud - 10 Minute Deployment ⚡

Get your newsletter running on Google Cloud in 10 minutes!

## Step 1: Create VM (3 minutes)

1. Go to: https://console.cloud.google.com
2. Navigate to: **Compute Engine** → **VM instances** → **Create Instance**
3. Configure:
   - **Name:** `newsletter-vm`
   - **Region:** `us-central1` (Iowa)
   - **Zone:** `us-central1-a`
   - **Machine type:** `e2-micro` (2 vCPU, 1 GB) ← **FREE TIER**
   - **Boot disk:** Ubuntu 22.04 LTS, 30 GB
4. Click **Create**

**Cost: $0/month** (Always Free tier)

---

## Step 2: Connect & Deploy (5 minutes)

1. Click **SSH** button next to your VM
2. Run this one command:

```bash
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/gcp-setup.sh | bash -s -- https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

**OR manually:**

```bash
# Update system
sudo apt update && sudo apt install -y python3 python3-pip git

# Clone your repo (replace with your URL)
git clone YOUR_REPO_URL nse-bse-newsletter
cd nse-bse-newsletter

# Run setup
./gcp-setup.sh
```

3. When prompted, test the newsletter → Check your email!

---

## Step 3: Done! ✅

Your newsletter is now running!

- ✅ Sends daily at **3:45 PM**
- ✅ Email to: **benjamin.prajwal57@gmail.com**
- ✅ Runs **forever** (auto-restart on failures)
- ✅ **$0/month** cost

---

## Quick Commands

```bash
# Check if running
sudo systemctl status newsletter-scheduler

# View logs
tail -f ~/nse-bse-newsletter/logs/scheduler.log

# Send test email now
cd ~/nse-bse-newsletter
python3 scheduler.py --now

# Restart service
sudo systemctl restart newsletter-scheduler
```

---

## Manual Setup (If You Prefer)

### 1. Create VM in Google Cloud Console

**Settings:**
- Region: us-central1 (Iowa) - **Required for free tier**
- Machine: e2-micro (1 GB RAM) - **Free tier eligible**
- OS: Ubuntu 22.04 LTS
- Disk: 30 GB standard

### 2. SSH and Install

```bash
# Click SSH button in GCP Console
# Then run:

sudo apt update
sudo apt install -y python3 python3-pip git

# Clone repo
git clone <your-repo-url> nse-bse-newsletter
cd nse-bse-newsletter

# Install dependencies
pip3 install -r requirements.txt

# Configure email (already done)
cp .env.example .env
nano .env  # Verify credentials are correct

# Test
python3 scheduler.py --now
```

### 3. Set Up Auto-Start

```bash
# Run deployment script
./deploy.sh

# Choose option 3 (systemd)
```

Done! The newsletter will now run daily.

---

## Monitoring

### Check Status

```bash
sudo systemctl status newsletter-scheduler
```

Should show: **Active (running)**

### View Live Logs

```bash
tail -f ~/nse-bse-newsletter/logs/scheduler.log
```

Press `Ctrl+C` to exit.

### Check What Was Scraped

```bash
ls -lh ~/nse-bse-newsletter/data/
cat ~/nse-bse-newsletter/data/nse_circulars.json
```

---

## Troubleshooting

### Newsletter not received?

```bash
# Check service status
sudo systemctl status newsletter-scheduler

# Check logs for errors
tail -50 ~/nse-bse-newsletter/logs/scheduler.log

# Test manually
cd ~/nse-bse-newsletter
python3 scheduler.py --now
```

### Service not running?

```bash
# Restart it
sudo systemctl restart newsletter-scheduler

# View error logs
sudo journalctl -u newsletter-scheduler -n 50
```

### Out of disk space?

```bash
# Check disk usage
df -h

# Clean old data
cd ~/nse-bse-newsletter/data
rm -f *.json  # Only if you don't need old data
```

---

## Cost Management

### Stay Free Forever

Your setup uses:
- ✅ e2-micro VM in us-central1 → **Free**
- ✅ 30 GB standard disk → **Free**
- ✅ Egress (outbound email) → **Minimal, free**

**Total: $0/month** within free tier limits

### Set Billing Alerts

1. Go to: **Billing** → **Budgets & alerts**
2. Create budget: **$1/month**
3. Set alerts at: **50%, 90%, 100%**

### Monitor Usage

Check: **Billing** → **Reports** to see current spending

---

## Stopping/Starting VM

### Stop VM (Newsletter won't run)

In GCP Console:
- Go to **VM instances**
- Select your VM
- Click **Stop**

### Start VM (Resume newsletter)

In GCP Console:
- Go to **VM instances**
- Select your VM
- Click **Start**

**Note:** Service auto-starts when VM boots!

---

## Update the Code

```bash
cd ~/nse-bse-newsletter
git pull
pip3 install -r requirements.txt --upgrade
sudo systemctl restart newsletter-scheduler
```

---

## Summary

You now have:

- ✅ Newsletter running on Google Cloud
- ✅ $0/month cost (Always Free tier)
- ✅ Auto-restart on failures
- ✅ Daily emails at 3:45 PM
- ✅ Professional, reliable setup

**Next:** Wait until 3:45 PM tomorrow to confirm the automated email! 📧

---

## Need More Details?

See [GOOGLE_CLOUD_DEPLOYMENT.md](GOOGLE_CLOUD_DEPLOYMENT.md) for comprehensive guide.

---

**Happy scraping!** 🚀
