#!/bin/bash
# Desktop Shortcut Installer for NSE/BSE Market Data Application (Linux)

clear
echo "=========================================="
echo "NSE/BSE Market Data Application"
echo "Desktop Shortcut Installer"
echo "=========================================="
echo ""

# Get the absolute path to the application directory
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine the desktop directory
if [ -n "$XDG_DESKTOP_DIR" ]; then
    DESKTOP_DIR="$XDG_DESKTOP_DIR"
elif [ -d "$HOME/Desktop" ]; then
    DESKTOP_DIR="$HOME/Desktop"
else
    DESKTOP_DIR="$HOME/Desktop"
    mkdir -p "$DESKTOP_DIR"
fi

# Also install to applications menu
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"

# Create the .desktop file content
DESKTOP_FILE="[Desktop Entry]
Version=1.0
Type=Application
Name=NSE-BSE Market App
Comment=Scrape, Process, and Analyze Stock Market Data
Exec=$APP_DIR/start_app.sh
Icon=$APP_DIR/app_icon.png
Path=$APP_DIR
Terminal=false
Categories=Office;Finance;
StartupNotify=true"

# Write to desktop
DESKTOP_SHORTCUT="$DESKTOP_DIR/nse-bse-market-app.desktop"
echo "$DESKTOP_FILE" > "$DESKTOP_SHORTCUT"
chmod +x "$DESKTOP_SHORTCUT"

# Write to applications menu
APPS_SHORTCUT="$APPS_DIR/nse-bse-market-app.desktop"
echo "$DESKTOP_FILE" > "$APPS_SHORTCUT"
chmod +x "$APPS_SHORTCUT"

# Try to mark as trusted (GNOME)
if command -v gio &> /dev/null; then
    gio set "$DESKTOP_SHORTCUT" metadata::trusted true 2>/dev/null
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$APPS_DIR" 2>/dev/null
fi

echo ""
echo "=========================================="
echo "SUCCESS!"
echo "=========================================="
echo ""
echo "Desktop shortcut created successfully!"
echo ""
echo "You can now find the application:"
echo "  • On your desktop: $(basename "$DESKTOP_SHORTCUT")"
echo "  • In applications menu: NSE-BSE Market App"
echo ""
echo "Location: $DESKTOP_SHORTCUT"
echo ""

# Check if we need to make it executable manually
if [ ! -x "$DESKTOP_SHORTCUT" ]; then
    echo "Note: You may need to right-click the desktop icon"
    echo "      and select 'Allow Launching' or 'Trust and Launch'"
    echo ""
fi

echo "=========================================="
echo ""
