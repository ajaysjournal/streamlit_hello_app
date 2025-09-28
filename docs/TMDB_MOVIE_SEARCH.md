# 🎬 TMDB Movie Search Implementation

## Overview

This document describes the implementation of the TMDB (The Movie Database) movie search feature in the Streamlit Hello App. The implementation follows test-driven development principles and provides a clean, user-friendly interface for searching movies.

## Architecture

### Components

1. **API Key Management** (`utils.py`)
   - Environment variable support
   - User input fallback
   - Health check validation

2. **TMDB Service** (`modules/tmdb_service.py`)
   - Movie search functionality
   - Poster URL generation
   - Data formatting

3. **Movie Search Page** (`modules/movie_search.py`)
   - User interface
   - Results display
   - Pagination

4. **Navigation Integration** (`main.py`, `components.py`)
   - Sidebar navigation
   - Routing

## API Key Management

### Environment Variable Support

```python
# Set in .env file
TMDB_API_KEY=your_tmdb_api_key_here
```

### User Input Fallback

If no API key is found in environment variables, the system prompts the user to enter one:

```python
api_key = st.text_input(
    "Enter your TMDB API key:",
    type="password",
    help="Get your API key from https://www.themoviedb.org/settings/api"
)
```

### Health Check Validation

The system validates API keys by making a test request to TMDB:

```python
def validate_tmdb_api_key(api_key: Optional[str]) -> str:
    """Validate TMDB API key by making a test request."""
    # Returns: 'valid', 'invalid', or 'error'
```

## TMDB Service

### Search Movies

```python
service = TmdbService(api_key)
results = service.search_movies('Inception', page=1)
```

### Response Format

```python
{
    'success': True,
    'movies': [
        {
            'id': 12345,
            'title': 'Inception',
            'overview': 'A mind-bending thriller...',
            'poster_url': 'https://image.tmdb.org/t/p/w500/poster.jpg',
            'release_year': '2010',
            'vote_average': 8.8,
            'vote_count': 25000
        }
    ],
    'current_page': 1,
    'total_pages': 5,
    'total_results': 100
}
```

## User Interface

### Search Form

- Clean, simple search input
- Real-time validation
- Help text and instructions

### Results Display

- Movie cards with posters
- Ratings and release years
- Pagination controls
- Error handling

### Error Messages

- Invalid API key
- Network errors
- No results found
- API rate limits

## Testing

### Test Structure

```
tests/
├── test_tmdb_utils.py      # API key management tests
├── test_tmdb_service.py     # TMDB service tests
└── test_movie_search.py     # UI component tests
```

### Test Coverage

- **42 total tests** covering all functionality
- **API Key Management**: Environment, user input, validation
- **Service Layer**: Search, error handling, data formatting
- **UI Components**: Movie cards, results, pagination
- **Edge Cases**: Missing data, network errors, invalid inputs

## Error Handling

### Network Errors

- Connection timeouts
- DNS resolution failures
- HTTP errors (4xx, 5xx)

### API Errors

- Invalid API key (401)
- Rate limiting (429)
- Server errors (5xx)

### User Input Errors

- Empty search queries
- Invalid characters
- Missing required fields

## Configuration

### Environment Variables

```bash
# Required for TMDB API access
TMDB_API_KEY=your_tmdb_api_key_here
```

### Dependencies

No additional dependencies required - uses existing `requests` library.

## Usage

### Getting Started

1. **Get TMDB API Key**:
   - Visit [TMDB Settings](https://www.themoviedb.org/settings/api)
   - Create account and request API key

2. **Set Environment Variable**:
   ```bash
   echo "TMDB_API_KEY=your_key_here" >> .env
   ```

3. **Run Application**:
   ```bash
   streamlit run src/streamlit_hello_app/main.py
   ```

4. **Navigate to Movie Search**:
   - Click "🎬 Movie Search" in sidebar
   - Enter movie title and search

### API Key Flow

1. **Environment Check**: Looks for `TMDB_API_KEY` in environment
2. **User Input**: Prompts for API key if not found
3. **Validation**: Tests API key with health check
4. **Error Handling**: Shows clear error messages

## Performance

### Caching

- Configuration data cached to reduce API calls
- Poster URLs generated efficiently

### Rate Limiting

- Respects TMDB API rate limits
- Error handling for rate limit exceeded

### Pagination

- Efficient pagination for large result sets
- Lazy loading of additional pages

## Security

### API Key Protection

- Password input type for API key entry
- No logging of API keys
- Secure environment variable handling

### Input Validation

- Query sanitization
- Parameter validation
- SQL injection prevention (N/A for this use case)

## Troubleshooting

### Common Issues

1. **"No TMDB API key found"**
   - Set `TMDB_API_KEY` environment variable
   - Or enter API key when prompted

2. **"Invalid API key"**
   - Check API key is correct
   - Ensure API key is active on TMDB

3. **"Connection error"**
   - Check internet connection
   - Verify TMDB API is accessible

4. **"No movies found"**
   - Try different search terms
   - Check spelling
   - Use more specific titles

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

### Potential Features

1. **Advanced Search**:
   - Filter by year, genre, rating
   - Sort by popularity, rating, date

2. **Movie Details**:
   - Full movie information
   - Cast and crew
   - Reviews and ratings

3. **Favorites**:
   - Save favorite movies
   - Create watchlists

4. **Recommendations**:
   - Similar movies
   - Trending movies
   - Personalized suggestions

### API Improvements

1. **Caching**:
   - Redis for search results
   - Local storage for user preferences

2. **Rate Limiting**:
   - Smart request batching
   - Exponential backoff

3. **Error Recovery**:
   - Automatic retry logic
   - Fallback data sources

## Contributing

### Adding New Features

1. **Write Tests First**:
   ```python
   def test_new_feature():
       # Test the new functionality
       assert new_feature() == expected_result
   ```

2. **Implement Feature**:
   ```python
   def new_feature():
       # Implementation
       return result
   ```

3. **Update Documentation**:
   - Add to this README
   - Update code comments
   - Add usage examples

### Code Standards

- Follow existing code style
- Add comprehensive docstrings
- Include type hints
- Write tests for all functions

## License

This implementation is part of the Streamlit Hello App project and follows the same license terms.
