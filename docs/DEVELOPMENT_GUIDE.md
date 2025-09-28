# 🚀 Streamlit Hello App Development Guide

## Overview

This guide provides comprehensive instructions for developing new features in the Streamlit Hello App, with special focus on API integrations and test-driven development.

## 🎯 Development Principles

### 1. Test-Driven Development (TDD)
- **Write tests first** before implementing functionality
- **Achieve >90% test coverage** for all new code
- **Mock external dependencies** to avoid rate limits and network issues
- **Test all error scenarios** including network failures and API errors

### 2. Clean Architecture
- **Separation of concerns** with clear module boundaries
- **Service layer pattern** for API integrations
- **Utility functions** for reusable functionality
- **UI components** for user interface

### 3. Security First
- **Never log sensitive data** (API keys, tokens, personal information)
- **Validate all inputs** before processing
- **Use secure storage** for credentials
- **Implement proper error handling** without exposing sensitive information

## 🏗️ Project Structure

```
streamlit_hello_app/
├── src/streamlit_hello_app/
│   ├── main.py                 # Main application entry point
│   ├── config.py              # Configuration management
│   ├── utils.py                # Utility functions
│   ├── components.py           # UI components
│   └── modules/
│       ├── dashboard.py        # Dashboard page
│       ├── data_explorer.py    # Data explorer page
│       ├── compound_interest.py # Compound interest calculator
│       ├── movie_search.py     # Movie search page
│       └── tmdb_service.py     # TMDB API service
├── tests/
│   ├── test_config.py          # Configuration tests
│   ├── test_utils.py           # Utility function tests
│   ├── test_tmdb_utils.py      # TMDB utility tests
│   ├── test_tmdb_service.py   # TMDB service tests
│   └── test_movie_search.py    # Movie search UI tests
├── docs/
│   ├── TMDB_MOVIE_SEARCH.md    # TMDB implementation docs
│   ├── TEST_DRIVEN_DEVELOPMENT.md # TDD guidelines
│   └── DEVELOPMENT_GUIDE.md    # This file
├── scripts/
│   └── run_tmdb_tests.py       # Test runner script
└── .cursor/
    └── rules/
        ├── TMDB_API_DEVELOPMENT.md # TMDB development rules
        └── API_INTEGRATION_DEVELOPMENT.md # API integration rules
```

## 🧪 Testing Framework

### Test Categories

#### 1. Unit Tests
- Test individual functions/methods
- Mock external dependencies
- Fast execution
- High coverage

#### 2. Integration Tests
- Test component interactions
- Test API integrations
- Mock external APIs
- Test data flow

#### 3. UI Tests
- Test Streamlit components
- Mock user interactions
- Test error states
- Test user experience

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_tmdb_*.py -v
pytest tests/test_movie_search.py -v

# Run with coverage
pytest tests/ --cov=src/streamlit_hello_app --cov-report=html

# Run TMDB tests specifically
python scripts/run_tmdb_tests.py
```

## 🔌 API Integration Development

### 1. Service Layer Pattern

```python
class ApiService:
    """Base class for API services."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.example.com"
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'Streamlit-Hello-App/1.0',
            'Accept': 'application/json'
        })
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make API request with comprehensive error handling."""
        try:
            response = self._session.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise ApiTimeoutError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise ApiConnectionError("Connection failed")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ApiAuthenticationError("Invalid API key")
            elif e.response.status_code == 429:
                raise ApiRateLimitError("Rate limit exceeded")
            else:
                raise ApiError(f"HTTP error: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ApiError(f"Request failed: {str(e)}")
```

### 2. API Key Management

```python
def get_api_key(service_name: str) -> Optional[str]:
    """Get API key with environment variable and user input fallback."""
    # 1. Check environment variable
    env_var = f"{service_name.upper()}_API_KEY"
    api_key = os.getenv(env_var)
    if api_key:
        return api_key
    
    # 2. Prompt user for input
    try:
        import streamlit as st
        api_key = st.text_input(
            f"Enter your {service_name} API key:",
            type="password",
            help=f"Get your API key from {service_name} settings"
        )
        return api_key if api_key else None
    except ImportError:
        return None

def validate_api_key(api_key: Optional[str], validation_endpoint: str) -> str:
    """Validate API key with health check."""
    if not api_key:
        return "error"
    
    try:
        response = requests.get(
            validation_endpoint,
            params={"api_key": api_key},
            timeout=10
        )
        
        if response.status_code == 200:
            return "valid"
        elif response.status_code == 401:
            return "invalid"
        else:
            return "error"
    except Exception:
        return "error"
```

### 3. Error Handling

```python
class ApiError(Exception):
    """Base exception for API errors."""
    pass

class ApiAuthenticationError(ApiError):
    """API authentication error."""
    pass

class ApiRateLimitError(ApiError):
    """API rate limit error."""
    pass

class ApiConnectionError(ApiError):
    """API connection error."""
    pass

class ApiTimeoutError(ApiError):
    """API timeout error."""
    pass

def handle_api_error(error: Exception) -> str:
    """Convert API errors to user-friendly messages."""
    if isinstance(error, ApiAuthenticationError):
        return "❌ Invalid API key. Please check your credentials."
    elif isinstance(error, ApiRateLimitError):
        return "❌ Rate limit exceeded. Please try again later."
    elif isinstance(error, ApiConnectionError):
        return "❌ Connection failed. Please check your internet connection."
    elif isinstance(error, ApiTimeoutError):
        return "❌ Request timed out. Please try again."
    else:
        return "❌ An unexpected error occurred. Please try again."
```

## 🎨 UI Development

### 1. Page Structure

```python
def render_page() -> None:
    """Render page with comprehensive error handling."""
    st.header("📊 Page Title")
    st.markdown("Page description")
    
    # Get API key
    api_key = get_api_key('service_name')
    
    if not api_key:
        st.error("❌ No API key found. Please set API_KEY environment variable or enter your API key.")
        st.info("Get your API key from [Service Settings](https://service.example.com/settings)")
        return
    
    # Validate API key
    validation_result = validate_api_key(api_key)
    
    if validation_result != "valid":
        if validation_result == "invalid":
            st.error("❌ Invalid API key. Please check your key and try again.")
        else:
            st.error("❌ Error validating API key. Please check your connection and try again.")
        st.info("Get your API key from [Service Settings](https://service.example.com/settings)")
        return
    
    # Main functionality
    with st.form("main_form"):
        # Form inputs
        user_input = st.text_input("Enter input:", placeholder="Example input")
        submit_button = st.form_submit_button("Submit", type="primary")
    
    # Handle form submission
    if submit_button and user_input:
        with st.spinner("Processing..."):
            try:
                service = ApiService(api_key)
                results = service.process_data(user_input)
                
                if results['success']:
                    display_results(results)
                else:
                    st.error(f"❌ Processing failed: {results['error']}")
            except Exception as e:
                logging.error(f"Processing error: {e}")
                st.error(f"❌ An unexpected error occurred: {str(e)}")
```

### 2. Results Display

```python
def display_results(results: Dict[str, Any]) -> None:
    """Display results with proper formatting."""
    if not results.get('data'):
        st.info("🔍 No results found. Try a different search term.")
        return
    
    # Results header
    st.success(f"✅ Found {len(results['data'])} result(s)")
    
    # Display results
    for item in results['data']:
        display_item_card(item)
    
    # Pagination if needed
    if results.get('total_pages', 1) > 1:
        display_pagination(results)
```

### 3. Error Messages

```python
def display_error_message(error: Exception):
    """Display user-friendly error messages."""
    if isinstance(error, ApiAuthenticationError):
        st.error("❌ Invalid API key. Please check your credentials.")
        st.info("Get your API key from [Service Settings](https://service.example.com/settings)")
    elif isinstance(error, ApiRateLimitError):
        st.error("❌ Rate limit exceeded. Please try again later.")
        st.info("You can make up to 100 requests per hour.")
    elif isinstance(error, ApiConnectionError):
        st.error("❌ Connection failed. Please check your internet connection.")
    else:
        st.error("❌ An unexpected error occurred. Please try again.")
```

## 🧪 Testing Implementation

### 1. Test Structure

```python
class TestApiService:
    """Test cases for API service."""
    
    @patch('requests.Session.get')
    def test_successful_api_call(self, mock_get):
        """Test successful API call."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": [{"id": 1, "title": "Test Item"}]
        }
        mock_get.return_value = mock_response
        
        # Act
        service = ApiService('test_key')
        result = service.get_data()
        
        # Assert
        assert result['success'] is True
        assert len(result['data']) == 1
        assert result['data'][0]['title'] == 'Test Item'
        mock_get.assert_called_once()
    
    @patch('requests.Session.get')
    def test_api_authentication_error(self, mock_get):
        """Test API authentication error."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = HTTPError("401 Client Error")
        mock_get.return_value = mock_response
        
        # Act & Assert
        service = ApiService('invalid_key')
        with pytest.raises(ApiAuthenticationError):
            service.get_data()
```

### 2. UI Testing

```python
class TestPageUI:
    """Test cases for page UI."""
    
    @patch('streamlit_hello_app.modules.page.get_api_key')
    @patch('streamlit_hello_app.modules.page.validate_api_key')
    def test_render_page_with_valid_api_key(self, mock_validate, mock_get_key):
        """Test page rendering with valid API key."""
        # Arrange
        mock_get_key.return_value = 'valid_key'
        mock_validate.return_value = 'valid'
        
        # Act
        render_page()
        
        # Assert
        mock_get_key.assert_called_once()
        mock_validate.assert_called_once_with('valid_key')
```

### 3. Error Handling Tests

```python
class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_validate_api_key_connection_error(self):
        """Test validation with connection error."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = ConnectionError("Connection failed")
            
            result = validate_api_key('test_key', 'https://api.test.com/validate')
            assert result == 'error'
    
    def test_api_service_connection_error(self):
        """Test API service with connection error."""
        with patch('requests.Session.get') as mock_get:
            mock_get.side_effect = ConnectionError("Connection failed")
            
            service = ApiService('test_key')
            with pytest.raises(ApiConnectionError):
                service.get_data()
```

## 🔧 Development Workflow

### 1. Feature Development

```bash
# 1. Create feature branch
git checkout -b feature/new-api-integration

# 2. Write failing tests first
def test_new_feature():
    assert new_feature() == expected_result

# 3. Run tests (should fail)
pytest tests/test_new_feature.py::test_new_feature -v

# 4. Write minimal implementation
def new_feature():
    return expected_result

# 5. Run tests (should pass)
pytest tests/test_new_feature.py::test_new_feature -v

# 6. Refactor while keeping tests green
# 7. Add more test cases
# 8. Repeat cycle
```

### 2. Bug Fixing

```bash
# 1. Write test that reproduces bug
def test_bug_reproduction():
    result = buggy_function()
    assert result == expected_result  # This will fail

# 2. Fix the bug
def buggy_function():
    return expected_result  # Fixed

# 3. Run test (should pass)
pytest tests/test_bug_fix.py::test_bug_reproduction -v
```

### 3. Refactoring

```bash
# 1. Ensure all tests pass
pytest tests/ -v

# 2. Refactor code
# 3. Run tests again
pytest tests/ -v

# 4. If tests fail, fix implementation
# 5. Repeat until all tests pass
```

## 📊 Code Quality

### 1. Linting and Formatting

```bash
# Run linting
flake8 src/streamlit_hello_app/

# Run formatting
black src/streamlit_hello_app/

# Run type checking
mypy src/streamlit_hello_app/
```

### 2. Coverage Requirements

```bash
# Run coverage analysis
pytest --cov=src/streamlit_hello_app --cov-report=html --cov-report=term

# Ensure coverage threshold
pytest --cov=src/streamlit_hello_app --cov-fail-under=90
```

### 3. Documentation

```python
def new_function(param1: str, param2: int) -> Dict[str, Any]:
    """
    Brief description of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: If param1 is invalid
        ConnectionError: If network connection fails
        
    Example:
        >>> result = new_function("test", 123)
        >>> print(result['data'])
    """
```

## 🚀 Deployment

### 1. Environment Configuration

```bash
# Required environment variables
API_KEY=your_api_key_here
API_BASE_URL=https://api.example.com
API_TIMEOUT=10
API_RETRY_COUNT=3
```

### 2. Dependencies

```python
# requirements.txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
requests>=2.31.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

### 3. Configuration Files

```python
# env.example
# API Keys
API_KEY=your_api_key_here
TMDB_API_KEY=your_tmdb_api_key_here

# Application Settings
STREAMLIT_APP_NAME="Streamlit Hello App"
STREAMLIT_APP_VERSION="0.1.0"
STREAMLIT_DEBUG=false
```

## 🎯 Best Practices

### 1. Code Organization
- **Single Responsibility**: Each function should have one clear purpose
- **DRY Principle**: Don't repeat yourself, extract common functionality
- **Clear Naming**: Use descriptive names for functions, variables, and classes
- **Consistent Style**: Follow existing code style and conventions

### 2. Error Handling
- **Fail Fast**: Validate inputs early and fail with clear messages
- **Graceful Degradation**: Handle errors gracefully without crashing
- **User-Friendly Messages**: Show clear, actionable error messages to users
- **Logging**: Log detailed errors for debugging while showing clean messages to users

### 3. Testing
- **Test Coverage**: Aim for >90% test coverage
- **Test Independence**: Each test should be independent and not rely on other tests
- **Mock External Dependencies**: Don't make real API calls in tests
- **Test Edge Cases**: Test error scenarios, edge cases, and boundary conditions

### 4. Security
- **Input Validation**: Validate all user inputs before processing
- **Secure Storage**: Never hardcode credentials, use environment variables
- **Error Information**: Don't expose sensitive information in error messages
- **Rate Limiting**: Respect API rate limits and implement proper throttling

## 🚨 Common Pitfalls

### 1. Testing
- ❌ Don't make real API calls in tests
- ❌ Don't skip error case testing
- ❌ Don't test implementation details

### 2. Error Handling
- ❌ Don't expose sensitive error information
- ❌ Don't ignore network errors
- ❌ Don't assume API responses are valid

### 3. Security
- ❌ Don't log API keys or sensitive data
- ❌ Don't hardcode credentials
- ❌ Don't skip input validation

### 4. Performance
- ❌ Don't ignore rate limits
- ❌ Don't skip caching opportunities
- ❌ Don't make unnecessary API calls

## 📚 Resources

### Documentation
- [Streamlit Documentation](https://docs.streamlit.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [requests Documentation](https://requests.readthedocs.io/)

### Testing
- [Test-Driven Development by Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [pytest Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [Mocking in Python](https://docs.python.org/3/library/unittest.mock.html)

### API Integration
- [REST API Best Practices](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [API Rate Limiting](https://cloud.google.com/architecture/rate-limiting-strategies-techniques)

---

**Remember**: Good code is not just about functionality - it's about maintainability, testability, and user experience. Always write tests first, handle errors gracefully, and prioritize security and performance.
