#!/bin/bash

# Quick Deployment Script for NSE/BSE Newsletter System
# This script automates the deployment process

set -e  # Exit on any error

echo "=========================================="
echo "NSE/BSE Newsletter Deployment Script"
echo "=========================================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Warning: This script is designed for Linux. You may need to adapt it for your OS."
fi

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi
echo "✓ Python $PYTHON_VERSION detected"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check if .env exists
if [ -f ".env" ]; then
    echo "✓ .env file found"
else
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠ IMPORTANT: Edit .env file with your Gmail credentials!"
    echo "  - GMAIL_ADDRESS"
    echo "  - GMAIL_APP_PASSWORD"
    echo "  - RECIPIENT_EMAIL"
    echo ""
    echo "Run: nano .env"
    echo ""
fi

# Create logs directory
mkdir -p logs
echo "✓ Logs directory created"
echo ""

# Create data directory
mkdir -p data
echo "✓ Data directory created"
echo ""

# Ask deployment method
echo "Choose deployment method:"
echo "1) Run in foreground (for testing)"
echo "2) Run with screen (background, easy)"
echo "3) Run with systemd (production, requires sudo)"
echo "4) Just test the newsletter"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "Starting newsletter scheduler in foreground..."
        echo "Press Ctrl+C to stop"
        echo ""
        python3 scheduler.py
        ;;
    2)
        echo ""
        echo "Starting newsletter scheduler with screen..."
        if ! command -v screen &> /dev/null; then
            echo "Installing screen..."
            sudo apt-get install -y screen
        fi
        screen -dmS newsletter python3 scheduler.py
        echo "✓ Scheduler started in screen session 'newsletter'"
        echo ""
        echo "Useful commands:"
        echo "  View session: screen -r newsletter"
        echo "  Detach: Press Ctrl+A then D"
        echo "  List sessions: screen -ls"
        ;;
    3)
        echo ""
        echo "Setting up systemd service..."

        # Get current user and directory
        CURRENT_USER=$(whoami)
        CURRENT_DIR=$(pwd)

        # Create temporary service file with correct paths
        sed "s|YOUR_USERNAME|$CURRENT_USER|g; s|/home/YOUR_USERNAME/nse-bse-newsletter|$CURRENT_DIR|g" \
            newsletter-scheduler.service > /tmp/newsletter-scheduler.service

        # Install service
        sudo cp /tmp/newsletter-scheduler.service /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable newsletter-scheduler
        sudo systemctl start newsletter-scheduler

        echo "✓ Systemd service installed and started"
        echo ""
        echo "Useful commands:"
        echo "  Check status: sudo systemctl status newsletter-scheduler"
        echo "  View logs: sudo journalctl -u newsletter-scheduler -f"
        echo "  Restart: sudo systemctl restart newsletter-scheduler"
        echo "  Stop: sudo systemctl stop newsletter-scheduler"
        ;;
    4)
        echo ""
        echo "Running test newsletter..."
        python3 scheduler.py --now
        echo ""
        echo "Check your email at: benjamin.prajwal57@gmail.com"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Deployment complete!"
echo "=========================================="
echo ""
echo "The scheduler will run daily at 3:45 PM"
echo "Newsletter will be sent to: benjamin.prajwal57@gmail.com"
echo ""
echo "Check logs at: logs/scheduler.log"
echo ""
