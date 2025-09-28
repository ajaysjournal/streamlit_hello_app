# 📚 Quick Reference Guide

## 🚀 Essential Commands

### Setup & Installation
```bash
# Clone repository
git clone https://github.com/yourusername/streamlit-hello-app.git
cd streamlit-hello-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Running the Application
```bash
# Easiest way
streamlit run run_app.py

# Alternative ways
streamlit run src/streamlit_hello_app/main.py
make run
streamlit-app  # After pip install -e .
```

### Stopping the Application
```bash
# In terminal where app is running
Ctrl + C

# Kill all Streamlit processes
pkill -f streamlit
```

## 🧪 Testing Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/streamlit_hello_app --cov-report=html

# Run specific test files
pytest tests/test_config.py
pytest tests/test_utils.py

# Run TMDB tests
python scripts/run_tmdb_tests.py
```

## 🔧 Development Commands

```bash
# Code formatting
black src/ tests/
isort src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/

# All quality checks
make lint
make format
make test
```

## 🎬 Movie Search Setup

```bash
# Set API key
export TMDB_API_KEY=your_key_here

# Or add to .env file
echo "TMDB_API_KEY=your_key_here" >> .env
```

## 📁 Project Structure

```
streamlit_hello_app/
├── src/streamlit_hello_app/     # Main application
│   ├── main.py                  # Entry point
│   ├── utils.py                 # Utility functions
│   ├── components.py            # UI components
│   └── modules/                 # Page modules
│       ├── dashboard.py         # Dashboard page
│       ├── data_explorer.py     # Data explorer
│       ├── compound_interest.py # Calculator
│       ├── movie_search.py      # Movie search
│       └── tmdb_service.py      # TMDB API service
├── tests/                       # Test files
├── docs/                        # Documentation
├── scripts/                     # Utility scripts
└── run_app.py                   # Simple launcher
```

## 🌐 Application URLs

- **Local Development**: http://localhost:8501
- **Alternative Port**: http://localhost:8502 (if 8501 is busy)

## 📊 Application Pages

1. **Dashboard** - Interactive metrics and charts
2. **Data Explorer** - CSV file analysis
3. **Compound Interest Calculator** - Financial planning
4. **Movie Search** - TMDB-powered movie search
5. **About** - Application information

## 🔑 Environment Variables

```bash
# Application settings
STREAMLIT_APP_NAME="Streamlit Hello App"
STREAMLIT_APP_VERSION="0.1.0"
STREAMLIT_DEBUG=false

# API keys
TMDB_API_KEY=your_tmdb_api_key_here

# Logging
LOG_LEVEL=INFO
```

## 🐛 Common Issues & Quick Fixes

### Import Errors
```bash
pip install -e .
```

### Port Already in Use
```bash
pkill -f streamlit
```

### Virtual Environment Issues
```bash
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Movie Search Not Working
```bash
# Check API key
echo $TMDB_API_KEY

# Set API key
export TMDB_API_KEY=your_key_here
```

## 📝 File Locations

- **Main App**: `src/streamlit_hello_app/main.py`
- **Configuration**: `src/streamlit_hello_app/config.py`
- **Utilities**: `src/streamlit_hello_app/utils.py`
- **Tests**: `tests/`
- **Documentation**: `docs/`
- **Requirements**: `requirements.txt`
- **Project Config**: `pyproject.toml`

## 🔍 Debugging

```bash
# Enable debug mode
export STREAMLIT_DEBUG=true
streamlit run run_app.py

# Check logs
streamlit run run_app.py --logger.level debug

# Verify installation
python --version
pip list
streamlit --version
```

## 📦 Package Management

```bash
# Install in development mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Update dependencies
pip install -e . --upgrade

# Uninstall
pip uninstall streamlit-hello-app
```

## 🚀 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Set main file: `run_app.py`
5. Deploy!

### Local Production
```bash
# Install production dependencies
pip install -r requirements.txt

# Run application
streamlit run run_app.py
```

---

**Need more help?** Check the [Troubleshooting Guide](TROUBLESHOOTING.md) or [Development Guide](DEVELOPMENT_GUIDE.md).
