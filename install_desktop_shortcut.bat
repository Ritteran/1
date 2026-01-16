@echo off
REM Desktop Shortcut Installer for NSE/BSE Market Data Application (Windows)

echo ==========================================
echo NSE/BSE Market Data Application
echo Desktop Shortcut Installer
echo ==========================================
echo.

REM Get the current directory
set "APP_DIR=%~dp0"
set "APP_DIR=%APP_DIR:~0,-1%"

REM Get the desktop path
set "DESKTOP=%USERPROFILE%\Desktop"

REM Create VBScript to make shortcut
set "SCRIPT=%TEMP%\CreateShortcut.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%SCRIPT%"
echo sLinkFile = "%DESKTOP%\NSE-BSE Market App.lnk" >> "%SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%SCRIPT%"
echo oLink.TargetPath = "%APP_DIR%\start_app.bat" >> "%SCRIPT%"
echo oLink.WorkingDirectory = "%APP_DIR%" >> "%SCRIPT%"
echo oLink.Description = "NSE/BSE Market Data Application - Scrape, Process, and Analyze Stock Data" >> "%SCRIPT%"
echo oLink.IconLocation = "%SystemRoot%\System32\shell32.dll,176" >> "%SCRIPT%"
echo oLink.Save >> "%SCRIPT%"

echo Creating desktop shortcut...
cscript //nologo "%SCRIPT%"
del "%SCRIPT%"

if exist "%DESKTOP%\NSE-BSE Market App.lnk" (
    echo.
    echo ==========================================
    echo SUCCESS!
    echo ==========================================
    echo.
    echo Desktop shortcut created successfully!
    echo.
    echo You can now find "NSE-BSE Market App" on your desktop.
    echo Double-click it to launch the application.
    echo.
    echo Location: %DESKTOP%\NSE-BSE Market App.lnk
    echo.
) else (
    echo.
    echo ==========================================
    echo ERROR
    echo ==========================================
    echo.
    echo Failed to create desktop shortcut.
    echo Please try running this script as Administrator.
    echo.
)

echo ==========================================
echo.
pause
