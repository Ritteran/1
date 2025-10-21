# Google Cloud Deployment Guide - NSE/BSE Newsletter

Complete step-by-step guide to deploy your newsletter system on Google Cloud Platform.

## Why Google Cloud?

- ✅ **Free Tier**: $300 credit for 90 days + Always Free tier
- ✅ **Always Free VM**: e2-micro instance (free forever in certain regions)
- ✅ **Reliable**: 99.95% uptime SLA
- ✅ **Simple**: Easy to set up and manage

## Cost Estimate

**Free Tier (Recommended):**
- e2-micro VM in us-central1, us-west1, or us-east1
- 30 GB standard persistent disk
- **Cost: $0/month** (within Always Free limits)

**If you exceed free tier:**
- e2-small VM: ~$13/month
- f1-micro VM: ~$4/month

---

## Step-by-Step Deployment

### Step 1: Set Up Google Cloud Account

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com
   - Sign in with your Google account

2. **Activate Free Trial:**
   - Click "Activate" for $300 free credit
   - Enter billing information (required but won't be charged during trial)

3. **Create a New Project:**
   - Click "Select a project" → "New Project"
   - Project name: `nse-bse-newsletter`
   - Click "Create"

### Step 2: Create a VM Instance

1. **Navigate to Compute Engine:**
   - In the left menu: **Compute Engine** → **VM instances**
   - Click "Create Instance"

2. **Configure VM Instance:**

   **Name:**
   ```
   newsletter-vm
   ```

   **Region & Zone:**
   ```
   Region: us-central1 (Iowa)
   Zone: us-central1-a
   ```
   *(Required for Always Free tier)*

   **Machine Configuration:**
   - Series: **E2**
   - Machine type: **e2-micro** (2 vCPU, 1 GB memory)
   - ✓ This qualifies for Always Free tier

   **Boot Disk:**
   - Click "Change"
   - Operating system: **Ubuntu**
   - Version: **Ubuntu 22.04 LTS**
   - Boot disk type: **Standard persistent disk**
   - Size: **30 GB** (max for free tier)
   - Click "Select"

   **Firewall:**
   - ☑ Allow HTTP traffic (optional)
   - ☐ Allow HTTPS traffic (not needed)

3. **Click "Create"**

   Wait 30-60 seconds for the VM to start.

### Step 3: Connect to Your VM

**Option A: Browser SSH (Easiest)**

1. In VM instances list, find your `newsletter-vm`
2. Click the **SSH** button
3. A browser window will open with terminal access

**Option B: Using gcloud CLI (Advanced)**

```bash
# Install gcloud CLI first
gcloud compute ssh newsletter-vm --zone=us-central1-a
```

### Step 4: Install the Newsletter System

Once connected via SSH, run these commands:

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3 python3-pip git

# Clone your repository
git clone <your-repository-url> nse-bse-newsletter
cd nse-bse-newsletter

# Install Python dependencies
pip3 install -r requirements.txt
```

### Step 5: Configure Email Credentials

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your credentials
nano .env
```

Add your credentials:
```
GMAIL_ADDRESS=benjamin.prajwal57@gmail.com
GMAIL_APP_PASSWORD=auar pukc lfey oizs
RECIPIENT_EMAIL=benjamin.prajwal57@gmail.com
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

### Step 6: Test the Newsletter

```bash
# Run a test
python3 scheduler.py --now
```

Check your email at benjamin.prajwal57@gmail.com!

If the test succeeds, proceed to the next step.

### Step 7: Set Up Automatic Startup

Use the deployment script to set up systemd:

```bash
# Run the deployment script
./deploy.sh
```

Choose **Option 3** (systemd) when prompted.

This will:
- Create a systemd service
- Start the scheduler
- Enable auto-start on VM reboot

### Step 8: Verify It's Running

```bash
# Check service status
sudo systemctl status newsletter-scheduler

# View logs
sudo journalctl -u newsletter-scheduler -f
```

You should see output indicating the scheduler is running.

---

## Managing Your VM

### Start/Stop VM to Save Costs

Even in the free tier, you might want to stop the VM when not needed:

**Stop VM:**
1. Go to **Compute Engine** → **VM instances**
2. Select your VM
3. Click **Stop**

**Start VM:**
1. Go to **Compute Engine** → **VM instances**
2. Select your VM
3. Click **Start**

**Note:** The newsletter won't run while the VM is stopped.

### Keep VM Running 24/7

For the newsletter to work daily:
- ✅ Keep the VM running
- ✅ e2-micro is in Always Free tier (no cost)
- ✅ Automatic restarts on failures

### SSH Back Into Your VM

```bash
# From Google Cloud Console
# Go to VM instances → Click "SSH"

# View logs
tail -f ~/nse-bse-newsletter/logs/scheduler.log

# Check scheduler status
sudo systemctl status newsletter-scheduler
```

---

## Monitoring and Maintenance

### View Logs

**Scheduler logs:**
```bash
tail -f ~/nse-bse-newsletter/logs/scheduler.log
```

**Systemd logs:**
```bash
sudo journalctl -u newsletter-scheduler -f
```

**Last 50 lines:**
```bash
sudo journalctl -u newsletter-scheduler -n 50
```

### Restart the Service

```bash
sudo systemctl restart newsletter-scheduler
```

### Update the Code

```bash
cd ~/nse-bse-newsletter
git pull
pip3 install -r requirements.txt --upgrade
sudo systemctl restart newsletter-scheduler
```

### Check VM Resource Usage

```bash
# CPU and memory
top

# Disk usage
df -h

# Specific to newsletter
ps aux | grep scheduler
```

---

## Setting Up Email Alerts (Optional)

Get notified if the VM goes down:

1. **Go to Monitoring in GCP Console:**
   - Navigation Menu → **Monitoring**

2. **Create an Alert:**
   - Go to **Alerting** → **Create Policy**
   - Metric: "VM Instance - Uptime"
   - Condition: Instance is down
   - Notification: Email to benjamin.prajwal57@gmail.com

3. **Save the alert policy**

---

## Troubleshooting

### Newsletter not sending?

```bash
# Check if service is running
sudo systemctl status newsletter-scheduler

# Check logs for errors
tail -50 ~/nse-bse-newsletter/logs/scheduler.log

# Restart service
sudo systemctl restart newsletter-scheduler

# Test manually
cd ~/nse-bse-newsletter
python3 scheduler.py --now
```

### Can't SSH into VM?

1. Check VM is running in Console
2. Try browser SSH from Console
3. Check firewall rules allow SSH (port 22)

### VM out of disk space?

```bash
# Check disk usage
df -h

# Clear old logs
sudo journalctl --vacuum-time=7d

# Clean old data
cd ~/nse-bse-newsletter/data
rm -f old_data_*.json
```

### Scraping errors (403)?

This is normal - NSE/BSE have anti-scraping protection. The system handles it gracefully and sends whatever data it can collect.

---

## Cost Monitoring

### Check Your Spending

1. **Go to Billing:**
   - Navigation Menu → **Billing** → **Reports**

2. **Set Budget Alerts:**
   - Go to **Budgets & alerts**
   - Create a budget: $1/month
   - Get alerts at 50%, 90%, 100%

### Stay in Free Tier

To remain free forever:
- ✅ Use e2-micro in us-central1, us-west1, or us-east1
- ✅ Keep disk ≤ 30 GB
- ✅ Don't create additional VMs
- ✅ Monitor your usage in Billing Reports

---

## Automated Deployment Script (Advanced)

Want to automate everything? Use this startup script when creating the VM:

**When creating VM, expand "Management, security, disks, networking, sole tenancy"**

**In Automation → Startup script, paste:**

```bash
#!/bin/bash
# Startup script for NSE/BSE Newsletter VM

# Update and install dependencies
apt update
apt install -y python3 python3-pip git

# Clone repository (replace with your repo URL)
cd /home/ubuntu
git clone <your-repo-url> nse-bse-newsletter
cd nse-bse-newsletter

# Install Python dependencies
pip3 install -r requirements.txt

# Configure .env (you'll need to add this separately)
cat > .env << 'EOF'
GMAIL_ADDRESS=benjamin.prajwal57@gmail.com
GMAIL_APP_PASSWORD=auar pukc lfey oizs
RECIPIENT_EMAIL=benjamin.prajwal57@gmail.com
EOF

# Set up systemd service
./deploy.sh << 'ANSWERS'
3
ANSWERS
```

---

## Quick Command Reference

| Task | Command |
|------|---------|
| SSH to VM | Click "SSH" in Console |
| Check service | `sudo systemctl status newsletter-scheduler` |
| View logs | `tail -f ~/nse-bse-newsletter/logs/scheduler.log` |
| Restart service | `sudo systemctl restart newsletter-scheduler` |
| Test newsletter | `python3 scheduler.py --now` |
| Update code | `cd ~/nse-bse-newsletter && git pull` |
| Stop VM | In Console: Select VM → Stop |
| Start VM | In Console: Select VM → Start |

---

## Summary

Your newsletter is now running on Google Cloud! Here's what happens:

- ✅ **Runs daily at 3:45 PM**
- ✅ **Sends email to benjamin.prajwal57@gmail.com**
- ✅ **Automatic restart if it crashes**
- ✅ **Auto-starts when VM reboots**
- ✅ **Free forever** (if using e2-micro in free tier region)

## Next Steps

1. ✅ Wait for 3:45 PM tomorrow to confirm automatic sending
2. ✅ Set up billing alerts to monitor costs
3. ✅ Check logs occasionally: `tail -f ~/nse-bse-newsletter/logs/scheduler.log`

---

## Need Help?

- **GCP Documentation:** https://cloud.google.com/compute/docs
- **Check Logs:** `sudo journalctl -u newsletter-scheduler -f`
- **Test Newsletter:** `python3 scheduler.py --now`

Happy scraping! 📊📧
