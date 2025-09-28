# Streamlit Hello App 🚀

A modern Python web application built with Streamlit, featuring interactive dashboards, data exploration, financial calculators, and movie search functionality.

## ✨ Features

- 🎨 **Interactive Dashboard** with metrics and visualizations
- 📊 **Data Explorer** for CSV file analysis
- 💰 **Compound Interest Calculator** for financial planning
- 🎬 **Movie Search** powered by TMDB API
- 🔧 **Clean Architecture** with modular design
- 📁 **Organized Pages** with sidebar navigation

## 🛠️ Technology Stack

- **Backend:** Python 3.11+
- **Web Framework:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualizations:** Plotly
- **Configuration:** PyTOML + Pydantic
- **Testing:** pytest

## 📋 Requirements

- Python 3.11 or later
- pip (Python package installer)

## 🚀 Quick Start

### 1. Setup

```bash
# Clone and navigate
git clone https://github.com/yourusername/streamlit-hello-app.git
cd streamlit-hello-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Run the Application

```bash
# Easiest way
streamlit run run_app.py

# Alternative ways
streamlit run src/streamlit_hello_app/main.py
make run
```

### 3. Access the App

Open your browser and go to `http://localhost:8501`

## 🎬 Movie Search Setup (Optional)

To use the movie search feature:

1. Get a free API key from [TMDB](https://www.themoviedb.org/settings/api)
2. Set environment variable: `export TMDB_API_KEY=your_key_here`
3. Or enter the key when prompted in the app

## 🛑 Stopping the Server

Press **Ctrl + C** in the terminal, or run:
```bash
pkill -f streamlit
```

## 📁 Project Structure

```
streamlit_hello_app/
├── src/streamlit_hello_app/     # Main application code
├── tests/                       # Test files
├── docs/                        # Documentation
├── run_app.py                   # Simple launcher
└── requirements.txt             # Dependencies
```

## 📚 Documentation

For detailed information, see the `docs/` folder:

- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Essential commands and shortcuts
- **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Development Guide](docs/DEVELOPMENT_GUIDE.md)** - Development workflow and best practices
- **[TMDB Movie Search](docs/TMDB_MOVIE_SEARCH.md)** - Movie search implementation
- **[Test-Driven Development](docs/TEST_DRIVEN_DEVELOPMENT.md)** - Testing guidelines

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/streamlit_hello_app --cov-report=html
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Happy coding! 🎉**
