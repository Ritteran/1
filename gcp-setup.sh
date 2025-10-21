#!/bin/bash

# Google Cloud Platform - One-Command Setup Script
# This script sets up the NSE/BSE newsletter system on a fresh GCP VM

set -e  # Exit on any error

echo "=========================================="
echo "Google Cloud - Newsletter Setup"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run as root"
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
sudo apt update -qq
sudo apt upgrade -y -qq
echo "✓ System updated"
echo ""

# Install dependencies
echo "📦 Installing Python and Git..."
sudo apt install -y python3 python3-pip git
echo "✓ Dependencies installed"
echo ""

# Clone repository
echo "📥 Cloning repository..."
REPO_URL=${1:-""}
if [ -z "$REPO_URL" ]; then
    echo "Please provide repository URL:"
    read -p "Repository URL: " REPO_URL
fi

if [ -d "nse-bse-newsletter" ]; then
    echo "Directory already exists. Pulling latest changes..."
    cd nse-bse-newsletter
    git pull
else
    git clone "$REPO_URL" nse-bse-newsletter
    cd nse-bse-newsletter
fi
echo "✓ Repository ready"
echo ""

# Install Python dependencies
echo "📦 Installing Python packages..."
pip3 install -q -r requirements.txt
echo "✓ Python packages installed"
echo ""

# Configure .env
if [ -f ".env" ]; then
    echo "✓ .env file already exists"
else
    echo "📝 Creating .env file..."
    cp .env.example .env

    # Check if we should use pre-configured values
    if [ -n "$GMAIL_ADDRESS" ] && [ -n "$GMAIL_APP_PASSWORD" ]; then
        # Use environment variables
        sed -i "s/your.email@gmail.com/$GMAIL_ADDRESS/" .env
        sed -i "s/your-16-digit-app-password/$GMAIL_APP_PASSWORD/" .env
        sed -i "s/benjamin.prajwal57@gmail.com/$RECIPIENT_EMAIL/" .env
        echo "✓ .env configured from environment variables"
    else
        # Use defaults for this specific deployment
        cat > .env << 'EOF'
GMAIL_ADDRESS=benjamin.prajwal57@gmail.com
GMAIL_APP_PASSWORD=auar pukc lfey oizs
RECIPIENT_EMAIL=benjamin.prajwal57@gmail.com
EOF
        echo "✓ .env configured with default credentials"
    fi
fi
echo ""

# Create directories
mkdir -p logs data
echo "✓ Created logs and data directories"
echo ""

# Test the newsletter
echo "📧 Running test newsletter..."
echo "This will send a test email to benjamin.prajwal57@gmail.com"
echo ""
read -p "Run test now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 scheduler.py --now
    echo ""
    echo "✓ Test complete! Check your email."
else
    echo "Skipping test."
fi
echo ""

# Set up systemd service
echo "🔧 Setting up systemd service..."

# Get current user and directory
CURRENT_USER=$(whoami)
CURRENT_DIR=$(pwd)

# Create service file
sudo tee /etc/systemd/system/newsletter-scheduler.service > /dev/null << EOF
[Unit]
Description=NSE/BSE Daily Newsletter Scheduler
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
ExecStart=/usr/bin/python3 $CURRENT_DIR/scheduler.py
Restart=always
RestartSec=10
StandardOutput=append:$CURRENT_DIR/logs/systemd.log
StandardError=append:$CURRENT_DIR/logs/systemd.log
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl enable newsletter-scheduler
sudo systemctl start newsletter-scheduler

echo "✓ Systemd service configured and started"
echo ""

# Check status
echo "📊 Service Status:"
sudo systemctl status newsletter-scheduler --no-pager -l
echo ""

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Your newsletter system is now running!"
echo ""
echo "📧 Emails will be sent to: benjamin.prajwal57@gmail.com"
echo "⏰ Daily at: 3:45 PM"
echo "📁 Logs location: $CURRENT_DIR/logs/scheduler.log"
echo ""
echo "Useful commands:"
echo "  Check status:    sudo systemctl status newsletter-scheduler"
echo "  View logs:       tail -f $CURRENT_DIR/logs/scheduler.log"
echo "  Restart:         sudo systemctl restart newsletter-scheduler"
echo "  Test now:        python3 scheduler.py --now"
echo ""
echo "=========================================="
