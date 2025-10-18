@echo off
REM AI Personal Assistant - Quick Launch Script for Windows

echo.
echo ========================================
echo   AI Personal Assistant 🧠
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
echo 📥 Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Launch the app
echo.
echo 🚀 Launching AI Personal Assistant...
echo.
echo 💡 The app will open in your browser
echo 💡 Press Ctrl+C to stop the server
echo.

streamlit run app.py

pause

