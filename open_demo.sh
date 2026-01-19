#!/bin/bash
# Quick Start Demo Launcher for Mac/Linux
# Double-click or run this file to view the interactive demo

echo ""
echo "Opening NIFTY 50 Analyzer Quick Start Demo..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Open demo in default browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$SCRIPT_DIR/QUICKSTART_DEMO.html"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$SCRIPT_DIR/QUICKSTART_DEMO.html" 2>/dev/null || \
    firefox "$SCRIPT_DIR/QUICKSTART_DEMO.html" 2>/dev/null || \
    google-chrome "$SCRIPT_DIR/QUICKSTART_DEMO.html" 2>/dev/null || \
    echo "Please open QUICKSTART_DEMO.html manually in your browser"
fi

sleep 2
