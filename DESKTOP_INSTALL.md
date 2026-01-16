# 🖥️ Desktop Shortcut Installation Guide

Make the NSE/BSE Market Data Application accessible from your desktop with a single click!

---

## 🚀 Quick Install

### Windows 🪟
1. Double-click **`install_desktop_shortcut.bat`**
2. Wait for "SUCCESS!" message
3. Find **"NSE-BSE Market App"** icon on your desktop
4. Double-click to launch!

### Linux 🐧
1. Open Terminal in the project folder
2. Run: **`chmod +x install_desktop_shortcut.sh`**
3. Run: **`./install_desktop_shortcut.sh`**
4. Find the app on your desktop and in your applications menu
5. Double-click to launch!

### Mac 🍎
1. Open Terminal in the project folder
2. Run: **`chmod +x install_desktop_shortcut_mac.sh`**
3. Run: **`./install_desktop_shortcut_mac.sh`**
4. Find **"NSE-BSE Market App.app"** on your desktop
5. Right-click → Open (first time only)
6. Click "Open" in the security dialog
7. From then on, just double-click to launch!

---

## ✨ What You Get

After installation, you'll have:

✅ **Desktop Icon**: Quick access from your desktop
✅ **One-Click Launch**: No need to navigate to project folder
✅ **Professional Look**: Proper application icon
✅ **Easy Access**: Find it like any other app

### Linux Users Also Get:
✅ **Applications Menu Entry**: Find it in your app launcher
✅ **Search Integration**: Search for "NSE" or "BSE"
✅ **System Integration**: Appears in system menus

---

## 📋 Detailed Installation Instructions

### Windows Detailed Steps:

1. **Locate the Installer**
   - Find `install_desktop_shortcut.bat` in the project folder
   - You can also right-click it and select "Run as Administrator" for better compatibility

2. **Run the Installer**
   - Double-click the file
   - A command window will open
   - Wait for the "SUCCESS!" message

3. **Verify Installation**
   - Check your desktop for "NSE-BSE Market App" shortcut
   - It should have a chart/graph icon

4. **Launch the Application**
   - Double-click the desktop shortcut
   - Your browser will open with the application
   - Start using immediately!

**Troubleshooting:**
- If it doesn't work, try running as Administrator
- Make sure you're in the correct project directory
- Check that `start_app.bat` exists in the same folder

---

### Linux Detailed Steps:

1. **Make the Installer Executable**
   ```bash
   cd /path/to/project
   chmod +x install_desktop_shortcut.sh
   ```

2. **Run the Installer**
   ```bash
   ./install_desktop_shortcut.sh
   ```

3. **Verify Installation**
   - Check your desktop for `nse-bse-market-app.desktop`
   - Check Applications menu for "NSE-BSE Market App"

4. **First Launch (GNOME/Ubuntu)**
   - Right-click the desktop icon
   - Select "Allow Launching" or "Trust and Launch"
   - Or double-click and allow when prompted

5. **Launch the Application**
   - Double-click the icon
   - Or launch from applications menu
   - Or search for "NSE-BSE Market"

**Where It's Installed:**
- Desktop: `~/Desktop/nse-bse-market-app.desktop`
- Apps Menu: `~/.local/share/applications/nse-bse-market-app.desktop`

**Troubleshooting:**
- If icon doesn't work, make sure it's executable: `chmod +x ~/Desktop/nse-bse-market-app.desktop`
- On GNOME, you may need to trust it: `gio set ~/Desktop/nse-bse-market-app.desktop metadata::trusted true`
- Make sure `start_app.sh` is executable: `chmod +x start_app.sh`

---

### Mac Detailed Steps:

1. **Make the Installer Executable**
   ```bash
   cd /path/to/project
   chmod +x install_desktop_shortcut_mac.sh
   ```

2. **Run the Installer**
   ```bash
   ./install_desktop_shortcut_mac.sh
   ```

3. **Verify Installation**
   - Check your desktop for "NSE-BSE Market App.app"
   - It should appear as a regular macOS application

4. **First Launch (Important!)**
   - **Right-click** the app (or Control+Click)
   - Select **"Open"** from the menu
   - Click **"Open"** in the security dialog
   - This is required for unsigned apps

5. **Subsequent Launches**
   - Just double-click like any other app
   - No security prompt after the first launch

**macOS Security Note:**
Since this app isn't from the App Store or a registered developer, macOS requires you to explicitly allow it on first launch. This is a standard security feature.

**Alternative Method:**
If right-click doesn't work:
1. Go to System Preferences → Security & Privacy
2. Click "Open Anyway" after trying to launch
3. Click "Open" in the confirmation dialog

**Troubleshooting:**
- Make sure `start_app.sh` is executable: `chmod +x start_app.sh`
- If Terminal says "permission denied", run: `chmod +x install_desktop_shortcut_mac.sh`
- On newer macOS, you might need to approve in System Preferences

---

## 🗑️ Uninstallation

If you want to remove the desktop shortcut:

### Windows:
- Double-click **`uninstall_desktop_shortcut.bat`**

### Linux/Mac:
- Run: **`./uninstall_desktop_shortcut.sh`**

Or simply delete the shortcut manually from your desktop!

---

## 🎨 Customizing the Icon (Optional)

### Windows:
1. Right-click the desktop shortcut
2. Select "Properties"
3. Click "Change Icon"
4. Browse to an icon file or choose from system icons
5. Click OK

### Linux:
1. Edit the .desktop file with a text editor
2. Change the `Icon=` line to point to your icon file
3. Save and refresh desktop

### Mac:
1. Find an icon image you like (.icns or .png)
2. Get Info on the app (Cmd+I)
3. Drag your icon to the icon in the Get Info window

---

## 📍 Shortcut Locations

### Windows:
- **Desktop**: `C:\Users\YourName\Desktop\NSE-BSE Market App.lnk`

### Linux:
- **Desktop**: `~/Desktop/nse-bse-market-app.desktop`
- **Apps Menu**: `~/.local/share/applications/nse-bse-market-app.desktop`

### Mac:
- **Desktop**: `~/Desktop/NSE-BSE Market App.app`

---

## ❓ Frequently Asked Questions

**Q: Can I move the project folder after creating the shortcut?**
A: No, the shortcut points to the current location. If you move the project, run the installer again.

**Q: Can I create multiple shortcuts?**
A: Yes! You can copy the desktop shortcut to other locations like your taskbar or start menu.

**Q: Will this work if I update the application?**
A: Yes! The shortcut points to `start_app.sh`/`start_app.bat`, which will always launch the latest version.

**Q: Can I rename the shortcut?**
A: Yes! Right-click → Rename (Windows/Linux) or Get Info → change name (Mac).

**Q: Does this install anything system-wide?**
A: No, it only creates a shortcut. Nothing is installed to system directories.

**Q: Can other users on my computer use this?**
A: The shortcut is user-specific. Each user needs to run the installer separately.

---

## 🔧 Manual Installation

If the automatic installer doesn't work, you can create a shortcut manually:

### Windows (Manual):
1. Right-click on desktop → New → Shortcut
2. Browse to `start_app.bat` in the project folder
3. Name it "NSE-BSE Market App"
4. Click Finish

### Linux (Manual):
Create a file `~/Desktop/nse-bse-market-app.desktop` with:
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=NSE-BSE Market App
Exec=/full/path/to/start_app.sh
Icon=utilities-terminal
Terminal=false
Categories=Office;Finance;
```
Make it executable: `chmod +x ~/Desktop/nse-bse-market-app.desktop`

### Mac (Manual):
1. Open Automator
2. Create new Application
3. Add "Run Shell Script" action
4. Enter: `cd /path/to/project && ./start_app.sh`
5. Save to Desktop as "NSE-BSE Market App"

---

## 🎉 You're Done!

Your desktop shortcut is now installed!

**Next Steps:**
1. Double-click the desktop icon
2. Wait for your browser to open
3. Start scraping and analyzing market data!

**Need Help?**
- See the main [README.md](README.md) for usage instructions
- Check [APPLICATION_GUIDE.md](APPLICATION_GUIDE.md) for features
- Review [QUICK_START.md](QUICK_START.md) for basics

---

*Enjoy quick access to your market data application!* 📊✨
