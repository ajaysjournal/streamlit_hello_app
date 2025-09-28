# Streamlit Hello App 🚀

A modern Python web application built with Streamlit, featuring Python 3.11+ support (compatible with 3.12+), PyTOML configuration management, and clean architecture principles.

## ✨ Features

- 🐍 **Python 3.11+** with modern type hints and syntax (compatible with 3.12+)
- 📦 **PyTOML** for configuration management
- 🎨 **Streamlit** for interactive web interface
- 📊 **Interactive visualizations** with Plotly
- 🔧 **Clean architecture** with Pydantic models
- 📈 **Data exploration** capabilities
- 💰 **Compound Interest Calculator** for financial planning
- 🎛️ **Configurable themes** and settings
- 📁 **Modular project structure** with organized pages

## ✅ Project Status

**Current Status: Fully Functional** 🚀

- ✅ **Package Installation**: Successfully installed with all dependencies
- ✅ **Test Suite**: 17 tests passing with comprehensive coverage
- ✅ **Streamlit Application**: Running successfully at `http://localhost:8501`
- ✅ **Configuration Management**: Modern PyTOML + Pydantic v2 setup
- ✅ **Development Tools**: Makefile, linting, formatting all configured
- ✅ **No Deprecation Warnings**: Updated to use modern Pydantic v2 patterns

## 🛠️ Technology Stack

- **Backend:** Python 3.11+ (compatible with 3.12+)
- **Web Framework:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualizations:** Plotly
- **Configuration:** PyTOML
- **Validation:** Pydantic v2
- **Environment Management:** python-dotenv
- **Build System:** Hatchling
- **Testing:** pytest with comprehensive coverage

## 📋 Requirements

- Python 3.11 or later (compatible with Python 3.12+)
- pip (Python package installer)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/streamlit-hello-app.git
cd streamlit-hello-app
```

### 2. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### 4. Run the Application

You have several options to run the application:

```bash
# Option 1: Using the package script (recommended after pip install -e .)
streamlit-app

# Option 2: Using the simple launcher script (easiest)
streamlit run run_app.py

# Option 3: Directly with Streamlit (now works with absolute imports)
streamlit run src/streamlit_hello_app/main.py

# Option 4: Using Makefile commands
make run              # Direct Streamlit run
make run-simple       # Using launcher script
make run-package      # Using package script
```

The application will start and be available at `http://localhost:8501`

> **Note**: The `streamlit-app` command requires the package to be installed in development mode (`pip install -e .`). If you haven't done this yet, use one of the other options.

### 5. Open Your Browser

Navigate to `http://localhost:8501` in your browser to view the application.

## 🛑 Stopping the Streamlit Server

When you're done with the application, you can stop the Streamlit server using several methods:

### Method 1: If running in foreground
If you started Streamlit in the foreground (not in background), simply press:
- **Ctrl + C** (on Mac/Linux)
- **Ctrl + Break** (on Windows)

### Method 2: Kill all Streamlit processes
```bash
pkill -f streamlit
```
This kills all processes containing "streamlit" in their command line.

### Method 3: Kill by port
```bash
lsof -ti:8501 | xargs kill
```
This finds the process using port 8501 and kills it.

### Method 4: More specific process killing
```bash
pkill -f "streamlit run"
```
This only kills processes that match "streamlit run" specifically.

### Method 5: If you know the process ID
```bash
kill <PID>
```
Replace `<PID>` with the actual process ID from `ps aux | grep streamlit`.

### Verification
You can verify the server is stopped by:
1. **Check processes**: `ps aux | grep streamlit` (should show no streamlit processes)
2. **Check port**: `lsof -i:8501` (should show port 8501 is free)
3. **Try accessing**: `http://localhost:8501` (should show connection refused)

## 📁 Project Structure

```
streamlit_hello_app/
├── src/streamlit_hello_app/          # Main package source code
│   ├── __init__.py                   # Package initialization
│   ├── main.py                       # Main application entry point
│   ├── config.py                     # Configuration management
│   ├── utils.py                      # Utility functions
│   └── components.py                 # Streamlit UI components
├── tests/                            # Test files
│   ├── __init__.py
│   ├── test_config.py                # Configuration tests
│   └── test_utils.py                 # Utility function tests
├── run_app.py                        # Simple launcher script
├── requirements.txt                  # Core dependencies for deployment
├── Makefile                          # Development commands
├── pyproject.toml                    # Project configuration and dependencies
├── README.md                         # This file
├── LICENSE                           # MIT License
├── .gitignore                        # Git ignore rules
├── env.example                       # Environment variables example
├── config.toml.example               # Configuration example
└── .streamlit/
    └── config.toml                   # Streamlit deployment configuration
```

## ⚙️ Configuration

The application uses PyTOML for configuration management. You can create a `config.toml` file to customize settings:

```toml
[app]
name = "My Custom App"
version = "1.0.0"
debug = true

[theme]
primary_color = "#FF6B6B"
background_color = "#FFFFFF"
secondary_background_color = "#F0F2F6"
text_color = "#404040"
```

## 🔧 Development

### Code Quality Tools

The project includes several code quality tools configured in `pyproject.toml`:

- **Black:** Code formatting
- **isort:** Import sorting
- **flake8:** Linting
- **mypy:** Type checking
- **pytest:** Testing framework

### Running Development Tools

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/streamlit_hello_app
```

### Pre-commit Hooks

Install pre-commit hooks to automatically run quality checks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

## 📊 Application Features

### Dashboard
- Interactive metrics and KPIs
- Sample charts and visualizations
- Interactive elements (sliders, selectboxes, checkboxes)

### Data Explorer
- CSV file upload and processing
- Data preview and summary statistics
- Interactive visualizations
- Sample data demonstrations

### About Page
- Application information
- Technology stack details
- Getting started instructions

## 🎨 Customization

### Themes
You can customize the application theme by modifying the configuration or using the sidebar theme selector.

### Adding New Pages
1. Add a new page to the `pages` list in `components.py`
2. Create a new render function for your page
3. Add the page to the main navigation logic in `main.py`

### Configuration Options
The application supports various configuration options through environment variables (with `STREAMLIT_` prefix) or TOML configuration files.

## 📦 Packaging

### Building the Package

```bash
# Build wheel
python -m build

# Build source distribution
python -m build --sdist
```

### Installing from Source

```bash
pip install .
```

## 🚀 Deployment

### Streamlit Cloud Deployment

1. **Push your code to GitHub**
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Connect your GitHub repository**
4. **Set the main file path**: `run_app.py`
5. **Deploy!**

### Other Deployment Platforms

The app can be deployed on any platform that supports Python and Streamlit:

- **Heroku**: Use the included `requirements.txt`
- **Railway**: Use the included `requirements.txt`
- **Docker**: Create a Dockerfile with the requirements
- **AWS/GCP/Azure**: Use container services

### Deployment Files Included

- `requirements.txt`: Core dependencies for deployment
- `run_app.py`: Simple launcher script for deployment
- `.streamlit/config.toml`: Streamlit configuration for deployment
- `pyproject.toml`: Modern Python packaging configuration

## 🧪 Testing

The project includes a comprehensive test suite with 17 tests covering all core functionality:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/streamlit_hello_app --cov-report=html

# Run specific test file
pytest tests/test_config.py
pytest tests/test_utils.py

# Run with verbose output
pytest -v

# Run tests using Makefile
make test
make test-cov
```

### Test Coverage
- **Configuration Management**: 100% coverage
- **Utility Functions**: 100% coverage
- **Total Test Suite**: 17 tests, all passing ✅

The test suite validates:
- Pydantic configuration models and validation
- TOML configuration loading
- Environment variable handling
- Logging setup and configuration
- Utility functions for file operations

### Recently Fixed Issues ✅
- **Pydantic v2 Migration**: Updated from deprecated class-based config to modern `ConfigDict`
- **Validation Error Handling**: Fixed test cases to work with Pydantic v2 validation errors
- **Logging Tests**: Resolved logging level comparison issues in test suite
- **TOML Structure**: Fixed configuration file structure in tests
- **Python Version Compatibility**: Updated to support Python 3.11+ while maintaining 3.12+ compatibility
- **Import Issues**: Fixed relative import errors by converting to absolute imports
- **Multiple Run Options**: Added simple launcher script and Makefile commands for easier execution
- **Deployment Dependencies**: Removed problematic `pytest-streamlit` dependency causing deployment failures
- **Deployment Files**: Added `requirements.txt` and `.streamlit/config.toml` for better deployment support
- **Package Script**: Fixed `streamlit-app` command by creating proper CLI entry point function

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Support

If you have any questions or need help, please:

- Open an issue on GitHub
- Contact the maintainer at your.email@example.com

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Plotly](https://plotly.com/) for interactive visualizations
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- [Hatchling](https://hatch.pypa.io/) for the build system

---

**Happy coding! 🎉**
