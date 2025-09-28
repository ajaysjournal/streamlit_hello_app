# Streamlit Hello App - Memory Bank

## 🎯 Project Overview

**Streamlit Hello App** is a modern Python web application built with Streamlit, featuring Python 3.11+ support, PyTOML configuration management, and clean architecture principles.

### Key Characteristics
- **Status**: Fully Functional 🚀
- **Python Version**: 3.11+ (compatible with 3.12+)
- **Framework**: Streamlit with Plotly visualizations
- **Architecture**: Modular with Pydantic v2 configuration
- **Testing**: 17 tests with comprehensive coverage
- **Package Management**: Modern PyTOML + Hatchling build system

## 📁 Project Structure

```
streamlit_hello_app/
├── src/streamlit_hello_app/          # Main package source code
│   ├── __init__.py                   # Package initialization
│   ├── main.py                       # Main application entry point
│   ├── config.py                     # Pydantic v2 configuration management
│   ├── utils.py                      # Utility functions
│   ├── components.py                 # Streamlit UI components
│   └── modules/                      # Feature modules
│       ├── dashboard.py              # Dashboard with metrics and charts
│       ├── data_explorer.py          # CSV upload and data analysis
│       ├── compound_interest.py      # Financial calculator
│       └── about.py                  # Application information
├── tests/                            # Test suite (17 tests)
│   ├── test_config.py                # Configuration tests
│   ├── test_utils.py                 # Utility function tests
│   └── test_compound_interest.py     # Calculator tests
├── run_app.py                        # Simple launcher script
├── requirements.txt                  # Core dependencies for deployment
├── pyproject.toml                    # Modern Python packaging configuration
├── Makefile                          # Development commands
└── .streamlit/config.toml            # Streamlit deployment configuration
```

## 🛠️ Technology Stack

### Core Dependencies
- **streamlit>=1.28.0** - Web framework
- **pandas>=2.0.0** - Data processing
- **numpy>=1.24.0** - Numerical computing
- **plotly>=5.15.0** - Interactive visualizations
- **pydantic>=2.0.0** - Data validation and settings
- **python-dotenv>=1.0.0** - Environment management

### Development Tools
- **pytest>=7.0.0** - Testing framework
- **black>=23.0.0** - Code formatting
- **isort>=5.12.0** - Import sorting
- **flake8>=6.0.0** - Linting
- **mypy>=1.5.0** - Type checking
- **pre-commit>=3.0.0** - Git hooks

## 🚀 Application Features

### 1. Dashboard Module (`modules/dashboard.py`)
- **Metrics Display**: Total Users, Active Sessions, Page Views, Conversion Rate
- **Interactive Charts**: Line charts and pie charts with Plotly
- **Interactive Elements**: Sliders, selectboxes, checkboxes, radio buttons
- **Theme Support**: Dark/light theme with Plotly integration

### 2. Data Explorer Module (`modules/data_explorer.py`)
- **CSV Upload**: File upload and processing
- **Data Preview**: DataFrame display with summary statistics
- **Visualizations**: Interactive charts based on uploaded data
- **Sample Data**: Built-in sample datasets for demonstration

### 3. Compound Interest Calculator (`modules/compound_interest.py`)
- **Financial Planning**: Calculate compound interest over time
- **Interactive Inputs**: Principal, rate, time, frequency inputs
- **Visualization**: Growth charts and detailed calculations
- **Export Options**: Results can be downloaded

### 4. About Module (`modules/about.py`)
- **Application Info**: Technology stack and features
- **Getting Started**: Instructions for new users
- **Configuration**: Current settings display

## ⚙️ Configuration Management

### Pydantic v2 Configuration (`config.py`)
```python
class AppConfig(BaseModel):
    app_name: str = "Streamlit Hello App"
    app_version: str = "0.1.0"
    debug: bool = False
    theme: Dict[str, Any] = {
        "primary_color": "#FF6B6B",
        "background_color": "#FFFFFF",
        "secondary_background_color": "#F0F2F6",
        "text_color": "#404040",
    }
    model_config = ConfigDict(env_prefix="STREAMLIT_")
```

### Configuration Sources
1. **TOML Files**: `config.toml` (see `config.toml.example`)
2. **Environment Variables**: `STREAMLIT_` prefix
3. **Default Values**: Built-in defaults in Pydantic model

## 🏃‍♂️ Running the Application

### Multiple Run Options
```bash
# Option 1: Direct Streamlit run (recommended for development)
streamlit run src/streamlit_hello_app/main.py

# Option 2: Using launcher script (easiest)
streamlit run run_app.py

# Option 3: Using package script (requires pip install -e .)
streamlit-app

# Option 4: Using Makefile
make run              # Direct Streamlit run
make run-simple       # Using launcher script
make run-package      # Using package script
```

### Development Setup
```bash
# Complete setup for new developers
make setup

# Or manual setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

## 🧪 Testing & Quality

### Test Suite
- **Total Tests**: 17 tests, all passing ✅
- **Coverage**: 100% for configuration and utilities
- **Test Files**: `test_config.py`, `test_utils.py`, `test_compound_interest.py`

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/streamlit_hello_app --cov-report=html

# Run specific test file
pytest tests/test_config.py

# Using Makefile
make test
make test-cov
```

### Code Quality Tools
```bash
# Format code
make format

# Lint code
make lint

# Run all CI checks
make ci-test

# Pre-commit hooks
make hooks
```

## 📦 Packaging & Deployment

### Package Configuration (`pyproject.toml`)
- **Build System**: Hatchling
- **Entry Point**: `streamlit-app = "streamlit_hello_app.main:cli_main"`
- **Python Version**: >=3.11
- **License**: MIT

### Deployment Options
1. **Streamlit Cloud**: Use `run_app.py` as main file
2. **Heroku/Railway**: Use `requirements.txt`
3. **Docker**: Create Dockerfile with requirements
4. **AWS/GCP/Azure**: Use container services

### Build Commands
```bash
# Build package
python -m build

# Install from source
pip install .

# Clean build artifacts
make clean-all
```

## 🔧 Development Workflow

### Makefile Commands
```bash
make help           # Show all available commands
make install        # Install package in development mode
make install-dev    # Install with development dependencies
make run            # Run Streamlit application
make test           # Run tests
make test-cov       # Run tests with coverage
make lint           # Run linting
make format         # Format code
make clean          # Clean temporary files
make setup          # Complete setup for new developers
```

### Pre-commit Hooks
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

## 🎨 UI Components & Theming

### Components (`components.py`)
- **Header**: Application title and navigation
- **Sidebar**: Page navigation and theme selector
- **Dark Theme**: CSS and Plotly theme integration
- **Plotly Themes**: Dark/light theme support for charts

### Theme Configuration
- **Primary Color**: Customizable via config
- **Background Colors**: Light/dark mode support
- **Plotly Integration**: Automatic theme application to charts
- **CSS Customization**: Minimal UI with hidden elements

## 🐛 Recent Fixes & Improvements

### Pydantic v2 Migration ✅
- Updated from deprecated class-based config to modern `ConfigDict`
- Fixed validation error handling in tests
- Resolved logging level comparison issues

### Import System ✅
- Fixed relative import errors by converting to absolute imports
- Added multiple run options for easier execution
- Created proper CLI entry point function

### Deployment Improvements ✅
- Removed problematic `pytest-streamlit` dependency
- Added `requirements.txt` for deployment
- Created `.streamlit/config.toml` for deployment configuration
- Fixed package script with proper CLI function

## 📝 Key Files & Their Purposes

### Core Application Files
- **`main.py`**: Application entry point, page routing, session state
- **`config.py`**: Pydantic v2 configuration management
- **`utils.py`**: Logging setup, environment loading, file operations
- **`components.py`**: Reusable UI components and theming

### Module Files
- **`dashboard.py`**: Metrics, charts, interactive elements
- **`data_explorer.py`**: CSV upload, data analysis, visualizations
- **`compound_interest.py`**: Financial calculator with charts
- **`about.py`**: Application information and help

### Configuration Files
- **`pyproject.toml`**: Modern Python packaging, dependencies, tools
- **`requirements.txt`**: Core dependencies for deployment
- **`Makefile`**: Development commands and workflows
- **`.streamlit/config.toml`**: Streamlit deployment configuration

## 🚨 Important Notes

### Python Version Compatibility
- **Minimum**: Python 3.11
- **Compatible**: Python 3.12+ and 3.13
- **Type Hints**: Modern Python syntax throughout

### Dependencies
- **Core**: Streamlit, Pandas, NumPy, Plotly, Pydantic v2
- **Dev**: pytest, black, isort, flake8, mypy, pre-commit
- **No Deprecated**: All dependencies are current and maintained

### Session State Management
- **Page Navigation**: Stored in `st.session_state.page`
- **Theme State**: Managed through sidebar components
- **Data Persistence**: CSV uploads and calculator results

## 🔍 Troubleshooting

### Common Issues
1. **Import Errors**: Use absolute imports, not relative
2. **Streamlit Not Found**: Ensure virtual environment is activated
3. **Port Conflicts**: Kill existing Streamlit processes with `pkill -f streamlit`
4. **Configuration Issues**: Check `config.toml` syntax and environment variables

### Debug Mode
- Set `debug: true` in configuration
- Use `STREAMLIT_DEBUG=true` environment variable
- Check logs for detailed error information

---

**Last Updated**: Current as of project state
**Status**: Fully functional with comprehensive test coverage
**Next Steps**: Ready for feature additions or deployment
