#!/bin/bash
# Start script for Streamlit Hello App

echo "🚀 Starting Streamlit Hello App..."
echo "📁 Working directory: $(pwd)"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -e .
fi

# Run the app
echo "🌟 Launching Streamlit app..."
streamlit run src/streamlit_hello_app/main.py

echo "👋 App stopped. Goodbye!"
