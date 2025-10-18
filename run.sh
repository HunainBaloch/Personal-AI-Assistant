#!/bin/bash
# AI Personal Assistant - Quick Launch Script for Linux/Mac

echo ""
echo "========================================"
echo "  AI Personal Assistant 🧠"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
echo "📥 Checking dependencies..."
pip show streamlit > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

# Launch the app
echo ""
echo "🚀 Launching AI Personal Assistant..."
echo ""
echo "💡 The app will open in your browser"
echo "💡 Press Ctrl+C to stop the server"
echo ""

streamlit run app.py

