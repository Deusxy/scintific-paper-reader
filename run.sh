#!/bin/bash

# NaturalReader Clone Run Script

echo "🗣️ Starting NaturalReader Clone..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Check if dependencies are installed
if [ ! -f "venv/bin/streamlit" ] && [ ! -f "venv/Scripts/streamlit.exe" ]; then
    echo "❌ Streamlit not found. Please run ./setup.sh first."
    exit 1
fi

# Run the app using the virtual environment
echo "🚀 Launching app..."
./venv/bin/python -m streamlit run app.py
