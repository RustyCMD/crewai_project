@echo off
echo ========================================
echo    Starting Idle Game
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Launching game...
echo.

REM Launch the game from the frontend directory
cd /d "%~dp0"
python frontend\main_window.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the game
    echo Check if all required dependencies are installed
    pause
)
