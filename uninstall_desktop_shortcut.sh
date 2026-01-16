#!/bin/bash
# Desktop Shortcut Uninstaller for NSE/BSE Market Data Application (Linux/Mac)

clear
echo "=========================================="
echo "NSE/BSE Market Data Application"
echo "Desktop Shortcut Uninstaller"
echo "=========================================="
echo ""

# Determine the desktop directory
if [ -n "$XDG_DESKTOP_DIR" ]; then
    DESKTOP_DIR="$XDG_DESKTOP_DIR"
elif [ -d "$HOME/Desktop" ]; then
    DESKTOP_DIR="$HOME/Desktop"
else
    DESKTOP_DIR="$HOME/Desktop"
fi

# Applications directory
APPS_DIR="$HOME/.local/share/applications"

# File paths
DESKTOP_SHORTCUT="$DESKTOP_DIR/nse-bse-market-app.desktop"
APPS_SHORTCUT="$APPS_DIR/nse-bse-market-app.desktop"
MAC_APP="$DESKTOP_DIR/NSE-BSE Market App.app"

REMOVED=0

# Remove desktop shortcut (Linux)
if [ -f "$DESKTOP_SHORTCUT" ]; then
    echo "Removing desktop shortcut..."
    rm "$DESKTOP_SHORTCUT"
    REMOVED=1
fi

# Remove applications menu entry (Linux)
if [ -f "$APPS_SHORTCUT" ]; then
    echo "Removing applications menu entry..."
    rm "$APPS_SHORTCUT"
    REMOVED=1
fi

# Remove Mac app bundle
if [ -d "$MAC_APP" ]; then
    echo "Removing application bundle..."
    rm -rf "$MAC_APP"
    REMOVED=1
fi

# Update desktop database (Linux)
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$APPS_DIR" 2>/dev/null
fi

echo ""
if [ $REMOVED -eq 1 ]; then
    echo "=========================================="
    echo "SUCCESS!"
    echo "=========================================="
    echo ""
    echo "Desktop shortcut(s) removed successfully!"
else
    echo "=========================================="
    echo "NOT FOUND"
    echo "=========================================="
    echo ""
    echo "No desktop shortcuts were found."
    echo "They may have been already removed."
fi
echo ""
echo "=========================================="
echo ""
