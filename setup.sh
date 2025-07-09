#!/bin/bash

# NaturalReader Clone Setup Script

echo "🗣️ Setting up NaturalReader Clone..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt_tab', quiet=True); nltk.download('punkt', quiet=True)"

echo "✅ Setup complete!"
echo ""
echo "🚀 To run the app, use one of these methods:"
echo ""
echo "Method 1 - Manual activation:"
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo ""
echo "Method 2 - Direct run:"
echo "  ./venv/bin/streamlit run app.py"
echo ""
echo "Method 3 - Using python -m:"
echo "  ./venv/bin/python -m streamlit run app.py"
echo ""
echo "The app will open in your browser at http://localhost:8501"
