@echo off
REM Launcher script for NSE/BSE Webscraper (Windows)

echo ==========================================
echo NSE/BSE Stock Market Scraper
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
if not exist "venv\installed.txt" (
    echo Installing dependencies... ^(This may take a few minutes^)
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    type nul > venv\installed.txt
    echo Dependencies installed!
    echo.
)

REM Start the application
echo ==========================================
echo Starting the web application...
echo ==========================================
echo.
echo The application will open in your web browser automatically.
echo If it doesn't open, go to: http://localhost:8501
echo.
echo To stop the application, press Ctrl+C
echo.

streamlit run app.py

REM Deactivate virtual environment on exit
call venv\Scripts\deactivate.bat

pause
