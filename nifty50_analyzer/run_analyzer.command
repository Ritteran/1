#!/bin/bash
# NIFTY 50 Stock Analyzer - Mac/Linux Launcher
# Double-click this file to run the analysis

clear

echo ""
echo "================================================================================"
echo "           NIFTY 50 STOCK ANALYZER - One-Click Launcher"
echo "================================================================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    echo "Or use: brew install python3 (if you have Homebrew)"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "[1/3] ✅ Checking Python installation..."
python3 --version
echo ""

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "[2/3] 🔧 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ ERROR: Failed to create virtual environment"
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo "✅ Virtual environment created successfully"
    echo ""
fi

# Activate virtual environment
echo "[2/3] 🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "[3/3] 📦 Installing required packages..."
pip install --quiet --upgrade pip
pip install --quiet pandas numpy pyyaml

echo ""
echo "================================================================================"
echo "                         🚀 Starting Analysis..."
echo "================================================================================"
echo ""

# Change to src directory and run analyzer
cd src
python3 main.py
EXIT_CODE=$?

# Return to root directory
cd ..

echo ""
echo "================================================================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "                    ✅ Analysis Complete!"
else
    echo "                    ❌ Analysis Failed (Exit code: $EXIT_CODE)"
fi
echo "================================================================================"
echo ""
read -p "Press Enter to exit..."

exit $EXIT_CODE
