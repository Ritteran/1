@echo off
REM Launcher for NSE/BSE Market Data Application (Windows)

cls
echo ==========================================
echo NSE/BSE Market Data Application
echo Full-Featured Desktop Application
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
    echo.
    python -m pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    type nul > venv\installed.txt
    echo Dependencies installed!
    echo.
)

REM Start the application
cls
echo ==========================================
echo Starting Application...
echo ==========================================
echo.
echo The application will open in your web browser.
echo If it doesn't open automatically, go to:
echo.
echo     http://localhost:8501
echo.
echo Features:
echo    - Scrape NSE/BSE data
echo    - Load and process data files
echo    - Advanced filtering and search
echo    - Interactive visualizations
echo    - Export in multiple formats
echo.
echo To stop the application, press Ctrl+C
echo.
echo ==========================================
echo.

streamlit run app_enhanced.py

REM Deactivate virtual environment on exit
call venv\Scripts\deactivate.bat

pause
