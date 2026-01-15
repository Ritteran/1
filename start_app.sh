#!/bin/bash
# Launcher for NSE/BSE Market Data Application (Unix/Linux/Mac)

clear
echo "=========================================="
echo "NSE/BSE Market Data Application"
echo "Full-Featured Desktop Application"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Error: Python 3 is not installed!"
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/installed.txt" ]; then
    echo "Installing dependencies... (This may take a few minutes)"
    echo ""
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    touch venv/installed.txt
    echo "✅ Dependencies installed!"
    echo ""
fi

# Start the application
clear
echo "=========================================="
echo "🚀 Starting Application..."
echo "=========================================="
echo ""
echo "The application will open in your web browser."
echo "If it doesn't open automatically, go to:"
echo ""
echo "    👉 http://localhost:8501"
echo ""
echo "📚 Features:"
echo "   • Scrape NSE/BSE data"
echo "   • Load and process data files"
echo "   • Advanced filtering and search"
echo "   • Interactive visualizations"
echo "   • Export in multiple formats"
echo ""
echo "To stop the application, press Ctrl+C"
echo ""
echo "=========================================="
echo ""

streamlit run app_enhanced.py

# Deactivate virtual environment on exit
deactivate
