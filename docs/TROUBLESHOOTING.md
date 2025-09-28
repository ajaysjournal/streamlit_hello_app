# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 🚀 Application Won't Start

#### Issue: "ModuleNotFoundError" or Import Errors
**Solution:**
```bash
# Make sure you're in the project directory
cd streamlit_hello_app

# Install in development mode
pip install -e .

# Then run
streamlit run run_app.py
```

#### Issue: "streamlit-app command not found"
**Solution:**
```bash
# Install the package first
pip install -e .

# Then use the command
streamlit-app
```

#### Issue: Port 8501 already in use
**Solution:**
```bash
# Kill existing Streamlit processes
pkill -f streamlit

# Or use a different port
streamlit run run_app.py --server.port 8502
```

### 🐍 Python Environment Issues

#### Issue: "python: command not found"
**Solution:**
```bash
# Install Python 3.11+ from python.org
# Or use conda:
conda create -n streamlit-app python=3.11
conda activate streamlit-app
```

#### Issue: Virtual environment not activating
**Solution:**
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate

# Verify activation
which python  # Should show venv path
```

#### Issue: Package installation fails
**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with verbose output
pip install -e . -v

# If still failing, try without cache
pip install -e . --no-cache-dir
```

### 🎬 Movie Search Issues

#### Issue: "No TMDB API key found"
**Solution:**
1. Get API key from [TMDB Settings](https://www.themoviedb.org/settings/api)
2. Set environment variable:
   ```bash
   export TMDB_API_KEY=your_key_here
   ```
3. Or enter key when prompted in the app

#### Issue: "Invalid TMDB API key"
**Solution:**
- Check your API key is correct
- Ensure API key is active on TMDB
- Try generating a new API key

#### Issue: "Connection failed" for movie search
**Solution:**
- Check your internet connection
- Verify TMDB API is accessible
- Try again in a few minutes

### 📊 Data Explorer Issues

#### Issue: CSV file won't upload
**Solution:**
- Check file size (should be < 200MB)
- Ensure file is a valid CSV format
- Try with a smaller test file first

#### Issue: "No data to display"
**Solution:**
- Upload a CSV file first
- Check file has data in the expected format
- Try the sample data option

### 🧪 Testing Issues

#### Issue: Tests fail with import errors
**Solution:**
```bash
# Install in development mode
pip install -e .

# Run tests from project root
pytest tests/
```

#### Issue: Coverage report not generating
**Solution:**
```bash
# Install coverage
pip install coverage

# Run with coverage
pytest --cov=src/streamlit_hello_app --cov-report=html
```

### 🔧 Development Issues

#### Issue: Code formatting fails
**Solution:**
```bash
# Install development dependencies
pip install -e ".[dev]"

# Format code
black src/ tests/
isort src/ tests/
```

#### Issue: Linting errors
**Solution:**
```bash
# Run linting
flake8 src/ tests/

# Fix common issues
# - Remove unused imports
# - Fix line length (max 88 characters)
# - Add missing docstrings
```

#### Issue: Type checking errors
**Solution:**
```bash
# Run type checking
mypy src/

# Fix type hints
# - Add return type annotations
# - Fix parameter types
# - Handle Optional types properly
```

### 🚀 Deployment Issues

#### Issue: Streamlit Cloud deployment fails
**Solution:**
1. Check `run_app.py` exists in root directory
2. Ensure `requirements.txt` is up to date
3. Verify all dependencies are listed
4. Check for any import errors in the logs

#### Issue: "Module not found" in deployment
**Solution:**
- Ensure all imports use absolute paths
- Check `pyproject.toml` has correct package structure
- Verify `src/streamlit_hello_app/__init__.py` exists

### 🎨 UI Issues

#### Issue: Dark theme not working
**Solution:**
- Clear browser cache
- Try refreshing the page
- Check if custom CSS is interfering

#### Issue: Charts not displaying
**Solution:**
- Check browser console for JavaScript errors
- Try a different browser
- Ensure Plotly is installed: `pip install plotly`

#### Issue: Sidebar navigation not working
**Solution:**
- Refresh the page
- Check browser console for errors
- Try clearing browser cache

### 🔍 Debugging Tips

#### Enable Debug Mode
```bash
# Set debug environment variable
export STREAMLIT_DEBUG=true

# Run with debug output
streamlit run run_app.py --logger.level debug
```

#### Check Application Logs
```bash
# View Streamlit logs
streamlit run run_app.py --logger.level debug 2>&1 | tee app.log
```

#### Verify Installation
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check Streamlit version
streamlit --version
```

### 🆘 Getting Help

#### Check Application Status
```bash
# Verify Streamlit is running
curl http://localhost:8501

# Check if port is in use
lsof -i:8501
```

#### Common Commands
```bash
# Stop all Streamlit processes
pkill -f streamlit

# Check running processes
ps aux | grep streamlit

# Clear Python cache
find . -type d -name "__pycache__" -delete
find . -name "*.pyc" -delete
```

#### Reset Environment
```bash
# Remove virtual environment
rm -rf venv

# Create new environment
python -m venv venv
source venv/bin/activate

# Reinstall everything
pip install -e .
```

### 📞 Support Resources

#### Documentation
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [TMDB API Documentation](https://developer.themoviedb.org/docs)

#### Community
- [Streamlit Community](https://discuss.streamlit.io/)
- [Python Community](https://www.python.org/community/)
- [GitHub Issues](https://github.com/yourusername/streamlit-hello-app/issues)

#### Quick Fixes
```bash
# Quick restart
pkill -f streamlit && streamlit run run_app.py

# Quick reinstall
pip install -e . --force-reinstall

# Quick test
pytest tests/ -v
```

---

**Still having issues?** Check the [Development Guide](DEVELOPMENT_GUIDE.md) or open an issue on GitHub.
