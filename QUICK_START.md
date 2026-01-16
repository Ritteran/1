# 🚀 Quick Start Guide (For Beginners)

## What does this tool do?

This tool downloads stock market data from NSE and BSE websites automatically. You just click a button and it collects all the information for you!

---

## 🖥️ Want a Desktop Shortcut? (Super Easy!)

**Make it even easier!** Install a desktop shortcut so you can launch the app with one click:

**Windows:**
- Double-click `install_desktop_shortcut.bat`

**Mac/Linux:**
- Double-click `install_desktop_shortcut.sh` (or run `./install_desktop_shortcut_mac.sh` on Mac)

**That's it!** Now you'll have an icon on your desktop. Just double-click to launch!

📖 **Detailed guide**: See [DESKTOP_INSTALL.md](DESKTOP_INSTALL.md)

---

## 📄 First Time Here? Start with the HTML Guide!

**Easiest way to get started:**
1. Find the file called `index.html` in the project folder
2. Double-click it to open in your web browser
3. You'll see a beautiful guide with:
   - Easy-to-follow instructions
   - Interactive command generator
   - Feature showcase
   - Troubleshooting tips

**No Python installation needed to view the guide!** It works in any web browser.

---

## ⚡ Ready to Use the Tool? Follow These 3 Steps

### Step 1: Make sure you have Python installed

**Don't have Python?** Download it here: https://www.python.org/downloads/

Click the big yellow button that says "Download Python". Install it like any other program.

✅ **Check if Python is installed:**
- Open Command Prompt (Windows) or Terminal (Mac/Linux)
- Type: `python --version`
- You should see something like "Python 3.11.0"

---

### Step 2: Start the application

**On Windows:**
1. Find the file called `start.bat` in the project folder
2. Double-click it
3. A black window will open - don't close it!
4. Your web browser will open automatically with the app

**On Mac or Linux:**
1. Open Terminal
2. Navigate to the project folder
3. Type: `./start.sh` and press Enter
4. Your web browser will open automatically with the app

⏱️ **First time only:** The app will install some required files. This takes 2-3 minutes.

---

### Step 3: Use the web interface

You'll see a web page that looks like an app. Here's how to use it:

1. **Left sidebar - Choose what you want:**
   - Select "NSE", "BSE", or "Both"
   - Check the boxes for the data you want
   - Slide the number bar to choose how many days

2. **Middle area - Start scraping:**
   - Click the big blue "🚀 Start Scraping" button
   - Wait while it collects data (you'll see a progress bar)

3. **Download your data:**
   - When it's done, you'll see tables with your data
   - Click any "Download" button to save the data
   - Choose CSV to open in Excel, or JSON for other uses

---

## 📥 What files will I get?

- **CSV files**: Open these in Microsoft Excel or Google Sheets
- **JSON files**: For programmers or data analysis tools
- **Excel files**: Native Excel format (.xlsx)

All files are saved in a folder called `data` inside the project folder.

---

## ❓ Common Questions

**Q: The browser says "localhost:8501" - is this the internet?**
A: No! This is running on YOUR computer only. It's completely private and secure. "localhost" means "this computer".

**Q: How do I stop the application?**
A: Just close your browser tab. The black window (terminal) will stop automatically, or you can close it.

**Q: Can I run this again later?**
A: Yes! Just double-click `start.bat` (Windows) or run `./start.sh` (Mac/Linux) again. It will be much faster the second time.

**Q: I got an error message. What do I do?**
A:
1. Make sure you have internet connection
2. Check that Python is installed
3. Look in the `logs` folder for error details
4. Try closing and restarting the application

**Q: Is this free?**
A: Yes, completely free!

**Q: Is my data safe?**
A: Yes! Everything runs on your computer. No data is sent anywhere except to NSE/BSE websites to download information.

---

## 🆘 Need Help?

**Application won't start:**
- Make sure Python is installed
- Right-click `start.bat` or `start.sh` and choose "Run as Administrator" (Windows) or use `sudo` (Mac/Linux)

**No data appears:**
- Check your internet connection
- Make sure you clicked at least one checkbox
- Try a shorter time range (like 7 days instead of 30)

**Browser didn't open:**
- Manually open your browser
- Go to: `http://localhost:8501`

---

## 💡 Tips for Success

1. ✅ Start with a small test: Select just one data type and 7 days
2. ✅ Don't close the black window (terminal) while the app is running
3. ✅ Download your data right away - it's not saved permanently in the app
4. ✅ Run the scraper during off-peak hours (not during market hours)

---

## 🎉 You're Ready!

That's all you need to know! The app is designed to be simple and user-friendly.

**Still confused?** Read the full README.md file for more detailed instructions.

---

**Remember:** You don't need to know any programming or technical stuff. Just click buttons and download your data! 🎯
