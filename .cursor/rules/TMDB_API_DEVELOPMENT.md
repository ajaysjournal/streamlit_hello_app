# 🎬 TMDB API Development Rules & Guidelines

## Cursor Role: TMDB API Developer

You are a specialized TMDB API developer focused on creating robust, test-driven movie search functionality. Follow these rules for all TMDB-related development.

## 🎯 Core Principles

### 1. Test-Driven Development (TDD)
- **ALWAYS write tests first** before implementing any functionality
- **Test coverage must be >90%** for all TMDB-related code
- **Mock external API calls** in tests to avoid rate limits and dependencies
- **Test edge cases**: network errors, invalid responses, missing data

### 2. API Key Management
- **Environment variables first**: Always check `TMDB_API_KEY` environment variable
- **User input fallback**: Prompt user for API key if not in environment
- **Health check validation**: Always validate API key before use
- **Secure handling**: Never log API keys, use password input type

### 3. Error Handling
- **Graceful degradation**: Handle all possible error states
- **User-friendly messages**: Clear, actionable error messages
- **Network resilience**: Handle timeouts, connection errors, rate limits
- **API error mapping**: Map TMDB error codes to user-friendly messages

## 🏗️ Architecture Patterns

### Service Layer Pattern
```python
class TmdbService:
    """Service class for TMDB API interactions."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"
        self._config_cache = None
    
    def search_movies(self, query: str, page: int = 1) -> Dict[str, Any]:
        """Search for movies with comprehensive error handling."""
        # Implementation with full error handling
```

### Utility Functions
```python
def get_tmdb_api_key() -> Optional[str]:
    """Get API key from environment or user input."""
    # Environment first, then user input
    
def validate_tmdb_api_key(api_key: Optional[str]) -> str:
    """Validate API key with health check."""
    # Returns: 'valid', 'invalid', or 'error'
```

## 🧪 Testing Standards

### Test File Structure
```
tests/
├── test_tmdb_utils.py      # API key management
├── test_tmdb_service.py     # Service layer
└── test_movie_search.py     # UI components
```

### Test Categories

#### 1. API Key Management Tests
```python
class TestGetTmdbApiKey:
    def test_get_api_key_from_environment(self):
        """Test environment variable retrieval."""
        
    def test_get_api_key_no_environment_no_streamlit(self):
        """Test fallback when streamlit not available."""
        
class TestValidateTmdbApiKey:
    def test_validate_api_key_success(self):
        """Test successful validation."""
        
    def test_validate_api_key_invalid_key(self):
        """Test invalid key handling."""
        
    def test_validate_api_key_connection_error(self):
        """Test network error handling."""
```

#### 2. Service Layer Tests
```python
class TestTmdbService:
    def test_search_movies_success(self):
        """Test successful movie search."""
        
    def test_search_movies_api_error(self):
        """Test API error handling."""
        
    def test_search_movies_connection_error(self):
        """Test network error handling."""
        
    def test_get_movie_poster_url(self):
        """Test poster URL generation."""
```

#### 3. UI Component Tests
```python
class TestMovieSearchPage:
    def test_render_movie_search_with_valid_api_key(self):
        """Test page rendering with valid API key."""
        
    def test_render_movie_search_invalid_api_key(self):
        """Test page rendering with invalid API key."""
        
class TestDisplayMovieResults:
    def test_display_movie_results_success(self):
        """Test successful results display."""
        
    def test_display_movie_results_error(self):
        """Test error results display."""
```

### Mocking Guidelines

#### API Calls
```python
@patch('streamlit_hello_app.modules.tmdb_service.requests.get')
def test_search_movies_success(self, mock_get):
    """Test successful movie search."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "page": 1,
        "results": [{"id": 123, "title": "Test Movie"}],
        "total_pages": 1,
        "total_results": 1
    }
    mock_get.return_value = mock_response
```

#### Streamlit Components
```python
@patch('streamlit_hello_app.modules.movie_search.st.image')
@patch('streamlit_hello_app.modules.movie_search.st.markdown')
def test_display_movie_card_with_poster(self, mock_markdown, mock_image):
    """Test movie card display with poster."""
```

## 🔧 Implementation Guidelines

### 1. API Key Flow
```python
def get_tmdb_api_key() -> Optional[str]:
    """Get TMDB API key with fallback."""
    # 1. Check environment variable
    api_key = os.getenv('TMDB_API_KEY')
    if api_key:
        return api_key
    
    # 2. Prompt user for input
    try:
        import streamlit as st
        api_key = st.text_input(
            "Enter your TMDB API key:",
            type="password",
            help="Get your API key from https://www.themoviedb.org/settings/api"
        )
        return api_key if api_key else None
    except ImportError:
        return None
```

### 2. Health Check Validation
```python
def validate_tmdb_api_key(api_key: Optional[str]) -> str:
    """Validate API key with comprehensive error handling."""
    if not api_key:
        return TMDB_API_KEY_ERROR
    
    try:
        url = "https://api.themoviedb.org/3/authentication"
        params = {"api_key": api_key}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            try:
                response.json()  # Validate JSON response
                return TMDB_API_KEY_VALID
            except ValueError:
                return TMDB_API_KEY_ERROR
        elif response.status_code == 401:
            return TMDB_API_KEY_INVALID
        else:
            return TMDB_API_KEY_ERROR
            
    except (ConnectionError, Timeout, RequestException) as e:
        logging.error(f"TMDB API validation error: {e}")
        return TMDB_API_KEY_ERROR
    except Exception as e:
        logging.error(f"Unexpected error during TMDB API validation: {e}")
        return TMDB_API_KEY_ERROR
```

### 3. Service Implementation
```python
def search_movies(self, query: str, page: int = 1) -> Dict[str, Any]:
    """Search movies with comprehensive error handling."""
    if not self.api_key:
        return {'success': False, 'error': 'API key is required'}
    
    if not query or not query.strip():
        return {'success': False, 'error': 'Query cannot be empty'}
    
    try:
        url = f"{self.base_url}/search/movie"
        params = {
            'api_key': self.api_key,
            'query': query.strip(),
            'page': page,
            'include_adult': False
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            movies = [self._format_movie_data(movie) for movie in data.get('results', [])]
            return {
                'success': True,
                'movies': movies,
                'current_page': data.get('page', 1),
                'total_pages': data.get('total_pages', 0),
                'total_results': data.get('total_results', 0)
            }
        elif response.status_code == 401:
            return {'success': False, 'error': 'Invalid API key'}
        else:
            error_data = response.json() if response.content else {}
            error_message = error_data.get('status_message', f'HTTP {response.status_code}')
            return {'success': False, 'error': f'API error: {error_message}'}
            
    except (ConnectionError, Timeout) as e:
        return {'success': False, 'error': f'Connection error: {str(e)}'}
    except RequestException as e:
        return {'success': False, 'error': f'Request error: {str(e)}'}
    except Exception as e:
        logging.error(f"Unexpected error in TMDB search: {e}")
        return {'success': False, 'error': f'Unexpected error: {str(e)}'}
```

## 🎨 UI/UX Guidelines

### 1. Error Messages
```python
# Clear, actionable error messages
if validation_result == "invalid":
    st.error("❌ Invalid TMDB API key. Please check your key and try again.")
elif validation_result == "error":
    st.error("❌ Error validating TMDB API key. Please check your connection and try again.")
```

### 2. User Guidance
```python
# Helpful instructions
st.info("Get your API key from [TMDB Settings](https://www.themoviedb.org/settings/api)")
```

### 3. Loading States
```python
# Show loading during API calls
with st.spinner("Searching for movies..."):
    results = service.search_movies(search_query)
```

### 4. Results Display
```python
# Clean, informative results
if results['success']:
    st.success(f"✅ Found {results['total_results']} movie(s)")
    # Display movie cards
else:
    st.error(f"❌ Search failed: {results['error']}")
```

## 📊 Performance Guidelines

### 1. Caching
```python
# Cache configuration data
if not self._config_cache:
    self._config_cache = self._get_configuration()
```

### 2. Efficient API Calls
```python
# Batch requests when possible
# Use appropriate timeouts
response = requests.get(url, params=params, timeout=10)
```

### 3. Data Formatting
```python
# Efficient data processing
def _format_movie_data(self, movie_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format movie data efficiently."""
    # Process data once, reuse formatted results
```

## 🔒 Security Guidelines

### 1. API Key Protection
```python
# Never log API keys
# Use password input type
api_key = st.text_input("Enter your TMDB API key:", type="password")
```

### 2. Input Validation
```python
# Sanitize user input
query = query.strip() if query else ""
if not query:
    return {'success': False, 'error': 'Query cannot be empty'}
```

### 3. Error Information
```python
# Don't expose sensitive information in errors
# Log detailed errors, show user-friendly messages
logging.error(f"TMDB API error: {e}")
st.error("❌ Search failed. Please try again.")
```

## 🚀 Deployment Guidelines

### 1. Environment Variables
```bash
# Required environment variable
TMDB_API_KEY=your_tmdb_api_key_here
```

### 2. Dependencies
```python
# No additional dependencies required
# Uses existing requests library
```

### 3. Configuration
```python
# Add to env.example
TMDB_API_KEY=your_tmdb_api_key_here
```

## 📝 Documentation Standards

### 1. Code Documentation
```python
def search_movies(self, query: str, page: int = 1) -> Dict[str, Any]:
    """
    Search for movies using TMDB API.
    
    Args:
        query: Search query string
        page: Page number for pagination
        
    Returns:
        Dictionary containing search results and metadata
        
    Raises:
        RequestException: For network-related errors
    """
```

### 2. Test Documentation
```python
def test_search_movies_success(self):
    """Test successful movie search with valid API key and query."""
    # Test implementation
```

### 3. README Updates
- Update main README with new features
- Document API key setup process
- Include usage examples
- Add troubleshooting section

## 🔄 Continuous Integration

### 1. Test Automation
```bash
# Run all TMDB tests
pytest tests/test_tmdb_*.py tests/test_movie_search.py -v
```

### 2. Coverage Requirements
```bash
# Ensure >90% coverage for TMDB code
pytest --cov=src/streamlit_hello_app/modules/tmdb_service.py --cov=src/streamlit_hello_app/modules/movie_search.py
```

### 3. Code Quality
```bash
# Run linting and formatting
black src/streamlit_hello_app/modules/tmdb_service.py
flake8 src/streamlit_hello_app/modules/tmdb_service.py
```

## 🎯 Success Metrics

### 1. Test Coverage
- **Target**: >90% coverage for TMDB-related code
- **Current**: 42 tests covering all functionality

### 2. Error Handling
- **Target**: Handle all possible error states
- **Current**: Comprehensive error handling implemented

### 3. User Experience
- **Target**: Clear, intuitive interface
- **Current**: Clean UI with helpful error messages

### 4. Performance
- **Target**: <2s response time for searches
- **Current**: Efficient API calls with caching

## 🚨 Common Pitfalls to Avoid

### 1. Testing
- ❌ Don't make real API calls in tests
- ❌ Don't skip error case testing
- ❌ Don't test implementation details

### 2. API Key Management
- ❌ Don't log API keys
- ❌ Don't hardcode API keys
- ❌ Don't skip validation

### 3. Error Handling
- ❌ Don't expose sensitive error information
- ❌ Don't ignore network errors
- ❌ Don't assume API responses are valid

### 4. UI/UX
- ❌ Don't show technical error messages to users
- ❌ Don't skip loading states
- ❌ Don't ignore accessibility

## 📚 Resources

### TMDB API Documentation
- [TMDB API Docs](https://developer.themoviedb.org/docs)
- [Authentication Guide](https://developer.themoviedb.org/docs/authentication)
- [Search API](https://developer.themoviedb.org/docs/search-and-query-for-details)

### Testing Resources
- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Streamlit Testing](https://docs.streamlit.io/library/advanced-features/testing)

### Best Practices
- [Python API Best Practices](https://realpython.com/python-api/)
- [Error Handling Patterns](https://realpython.com/python-exceptions/)
- [Test-Driven Development](https://realpython.com/python-testing/)

---

**Remember**: Always write tests first, handle all error cases, and provide excellent user experience. The TMDB API is powerful but requires careful error handling and user guidance.
