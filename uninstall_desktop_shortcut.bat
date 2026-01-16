@echo off
REM Desktop Shortcut Uninstaller for NSE/BSE Market Data Application (Windows)

echo ==========================================
echo NSE/BSE Market Data Application
echo Desktop Shortcut Uninstaller
echo ==========================================
echo.

REM Get the desktop path
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\NSE-BSE Market App.lnk"

if exist "%SHORTCUT%" (
    echo Removing desktop shortcut...
    del "%SHORTCUT%"

    if not exist "%SHORTCUT%" (
        echo.
        echo ==========================================
        echo SUCCESS!
        echo ==========================================
        echo.
        echo Desktop shortcut removed successfully!
        echo.
    ) else (
        echo.
        echo ==========================================
        echo ERROR
        echo ==========================================
        echo.
        echo Failed to remove desktop shortcut.
        echo Please try deleting it manually.
        echo.
    )
) else (
    echo.
    echo ==========================================
    echo NOT FOUND
    echo ==========================================
    echo.
    echo Desktop shortcut not found.
    echo It may have been already removed.
    echo.
)

echo ==========================================
echo.
pause
