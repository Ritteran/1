@echo off
REM NIFTY 50 Stock Analyzer - Windows Launcher
REM Double-click this file to run the analysis

echo.
echo ================================================================================
echo           NIFTY 50 STOCK ANALYZER - One-Click Launcher
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version
echo.

REM Check if virtual environment exists, create if not
if not exist "venv\" (
    echo [2/3] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
    echo.
)

REM Activate virtual environment
echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo [3/3] Installing required packages...
pip install --quiet --upgrade pip
pip install --quiet pandas numpy pyyaml

echo.
echo ================================================================================
echo                         Starting Analysis...
echo ================================================================================
echo.

REM Change to src directory and run analyzer
cd src
python main.py

REM Return to root directory
cd ..

echo.
echo ================================================================================
echo                    Analysis Complete - Press any key to exit
echo ================================================================================
pause
