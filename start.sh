#!/bin/bash
# Launcher script for NSE/BSE Webscraper (Unix/Linux/Mac)

echo "=========================================="
echo "NSE/BSE Stock Market Scraper"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed!"
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

echo "Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/installed.txt" ]; then
    echo "Installing dependencies... (This may take a few minutes)"
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/installed.txt
    echo "Dependencies installed!"
    echo ""
fi

# Start the application
echo "=========================================="
echo "Starting the web application..."
echo "=========================================="
echo ""
echo "The application will open in your web browser automatically."
echo "If it doesn't open, go to: http://localhost:8501"
echo ""
echo "To stop the application, press Ctrl+C"
echo ""

streamlit run app.py

# Deactivate virtual environment on exit
deactivate
