#!/bin/bash
# Desktop Shortcut Installer for NSE/BSE Market Data Application (macOS)

clear
echo "=========================================="
echo "NSE/BSE Market Data Application"
echo "Desktop Shortcut Installer (macOS)"
echo "=========================================="
echo ""

# Get the absolute path to the application directory
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Desktop directory
DESKTOP_DIR="$HOME/Desktop"

# Create an AppleScript application
APP_NAME="NSE-BSE Market App"
APP_BUNDLE="$DESKTOP_DIR/$APP_NAME.app"

echo "Creating application bundle..."

# Create app structure
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Create the launcher script
LAUNCHER="$APP_BUNDLE/Contents/MacOS/launcher"
cat > "$LAUNCHER" << 'LAUNCHER_EOF'
#!/bin/bash
APP_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$APP_DIR"
./start_app.sh
LAUNCHER_EOF

# Make launcher executable
chmod +x "$LAUNCHER"

# Create Info.plist
PLIST="$APP_BUNDLE/Contents/Info.plist"
cat > "$PLIST" << PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleName</key>
    <string>NSE-BSE Market App</string>
    <key>CFBundleDisplayName</key>
    <string>NSE-BSE Market App</string>
    <key>CFBundleIdentifier</key>
    <string>com.local.nse-bse-market-app</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.10</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
PLIST_EOF

# Create a symbolic link to the actual app directory in the bundle
ln -sf "$APP_DIR" "$APP_BUNDLE/Contents/Resources/app"

echo ""
echo "=========================================="
echo "SUCCESS!"
echo "=========================================="
echo ""
echo "Desktop application created successfully!"
echo ""
echo "You can now find '$APP_NAME.app' on your desktop."
echo "Double-click it to launch the application."
echo ""
echo "Location: $APP_BUNDLE"
echo ""
echo "Note: On first launch, you may need to:"
echo "  1. Right-click the app"
echo "  2. Select 'Open'"
echo "  3. Click 'Open' in the security dialog"
echo ""
echo "This is a standard macOS security feature for"
echo "applications not from the App Store."
echo ""
echo "=========================================="
echo ""
