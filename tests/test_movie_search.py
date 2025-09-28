"""Tests for movie search page functionality."""

import pytest
from unittest.mock import patch, MagicMock
import streamlit as st

from streamlit_hello_app.modules.movie_search import (
    render_movie_search,
    display_movie_results,
    display_movie_card,
    format_movie_data
)


class TestMovieSearchPage:
    """Test cases for movie search page."""
    
    @patch('streamlit_hello_app.modules.movie_search.get_tmdb_api_key')
    @patch('streamlit_hello_app.modules.movie_search.validate_tmdb_api_key')
    @patch('streamlit_hello_app.modules.movie_search.st.text_input')
    @patch('streamlit_hello_app.modules.movie_search.st.button')
    def test_render_movie_search_with_valid_api_key(self, mock_button, mock_text_input, 
                                                   mock_validate, mock_get_key):
        """Test rendering movie search with valid API key."""
        # Mock API key management
        mock_get_key.return_value = 'valid_api_key'
        mock_validate.return_value = 'valid'
        
        # Mock user input
        mock_text_input.return_value = 'Inception'
        mock_button.return_value = True
        
        # Mock successful search results
        with patch('streamlit_hello_app.modules.movie_search.TmdbService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.search_movies.return_value = {
                'success': True,
                'movies': [
                    {
                        'id': 12345,
                        'title': 'Inception',
                        'overview': 'A mind-bending thriller',
                        'poster_url': 'https://example.com/poster.jpg',
                        'release_year': '2010',
                        'vote_average': 8.8,
                        'vote_count': 25000
                    }
                ],
                'current_page': 1,
                'total_pages': 1,
                'total_results': 1
            }
            
            # This would normally be called by Streamlit
            # We're testing the logic flow
            render_movie_search()
            
            # Verify API key was retrieved and validated
            mock_get_key.assert_called_once()
            mock_validate.assert_called_once_with('valid_api_key')
    
    @patch('streamlit_hello_app.modules.movie_search.get_tmdb_api_key')
    @patch('streamlit_hello_app.modules.movie_search.validate_tmdb_api_key')
    @patch('streamlit_hello_app.modules.movie_search.st.text_input')
    def test_render_movie_search_invalid_api_key(self, mock_text_input, mock_validate, mock_get_key):
        """Test rendering movie search with invalid API key."""
        # Mock API key management
        mock_get_key.return_value = 'invalid_api_key'
        mock_validate.return_value = 'invalid'
        
        # Mock user input for API key
        mock_text_input.side_effect = ['invalid_api_key', 'Inception']
        
        render_movie_search()
        
        # Verify API key validation was called
        mock_validate.assert_called_once_with('invalid_api_key')
    
    @patch('streamlit_hello_app.modules.movie_search.get_tmdb_api_key')
    @patch('streamlit_hello_app.modules.movie_search.validate_tmdb_api_key')
    def test_render_movie_search_no_api_key(self, mock_validate, mock_get_key):
        """Test rendering movie search with no API key."""
        # Mock no API key available
        mock_get_key.return_value = None
        mock_validate.return_value = 'error'
        
        render_movie_search()
        
        # Verify API key retrieval was attempted
        mock_get_key.assert_called_once()


class TestDisplayMovieResults:
    """Test cases for display_movie_results function."""
    
    @patch('streamlit_hello_app.modules.movie_search.st.columns')
    @patch('streamlit_hello_app.modules.movie_search.st.button')
    def test_display_movie_results_success(self, mock_button, mock_columns):
        """Test displaying successful movie search results."""
        # Mock columns
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]
        
        # Mock pagination buttons
        mock_button.side_effect = [False, False]  # No pagination buttons clicked
        
        results = {
            'success': True,
            'movies': [
                {
                    'id': 12345,
                    'title': 'Inception',
                    'overview': 'A mind-bending thriller',
                    'poster_url': 'https://example.com/poster.jpg',
                    'release_year': '2010',
                    'vote_average': 8.8,
                    'vote_count': 25000
                }
            ],
            'current_page': 1,
            'total_pages': 1,
            'total_results': 1
        }
        
        display_movie_results(results)
        
        # Verify columns were created
        mock_columns.assert_called()
    
    def test_display_movie_results_no_results(self):
        """Test displaying no search results."""
        results = {
            'success': True,
            'movies': [],
            'current_page': 1,
            'total_pages': 0,
            'total_results': 0
        }
        
        # Should not raise any exceptions
        display_movie_results(results)
    
    def test_display_movie_results_error(self):
        """Test displaying error results."""
        results = {
            'success': False,
            'error': 'API key is invalid'
        }
        
        # Should not raise any exceptions
        display_movie_results(results)


class TestDisplayMovieCard:
    """Test cases for display_movie_card function."""
    
    @patch('streamlit_hello_app.modules.movie_search.st.image')
    @patch('streamlit_hello_app.modules.movie_search.st.markdown')
    def test_display_movie_card_with_poster(self, mock_markdown, mock_image):
        """Test displaying movie card with poster."""
        movie = {
            'id': 12345,
            'title': 'Inception',
            'overview': 'A mind-bending thriller',
            'poster_url': 'https://example.com/poster.jpg',
            'release_year': '2010',
            'vote_average': 8.8,
            'vote_count': 25000
        }
        
        display_movie_card(movie)
        
        # Verify image was displayed
        mock_image.assert_called_once_with('https://example.com/poster.jpg', width=200, caption='Inception')
        
        # Verify markdown was called for title and details
        assert mock_markdown.call_count >= 2  # Title and details
    
    @patch('streamlit_hello_app.modules.movie_search.st.image')
    @patch('streamlit_hello_app.modules.movie_search.st.markdown')
    def test_display_movie_card_without_poster(self, mock_markdown, mock_image):
        """Test displaying movie card without poster."""
        movie = {
            'id': 12345,
            'title': 'Inception',
            'overview': 'A mind-bending thriller',
            'poster_url': None,
            'release_year': '2010',
            'vote_average': 8.8,
            'vote_count': 25000
        }
        
        display_movie_card(movie)
        
        # Verify placeholder image was displayed
        mock_image.assert_called_once_with(
            'https://via.placeholder.com/200x300/404040/FFFFFF?text=No+Poster',
            width=200,
            caption='No poster available'
        )
        
        # Verify markdown was called for title and details
        assert mock_markdown.call_count >= 2


class TestFormatMovieData:
    """Test cases for format_movie_data function."""
    
    def test_format_movie_data_complete(self):
        """Test formatting complete movie data."""
        raw_movie = {
            'id': 12345,
            'title': 'Inception',
            'overview': 'A mind-bending thriller about dreams',
            'poster_path': '/test_poster.jpg',
            'release_date': '2010-07-16',
            'vote_average': 8.8,
            'vote_count': 25000
        }
        
        formatted = format_movie_data(raw_movie, 'https://example.com/poster.jpg')
        
        assert formatted['id'] == 12345
        assert formatted['title'] == 'Inception'
        assert formatted['overview'] == 'A mind-bending thriller about dreams'
        assert formatted['poster_url'] == 'https://example.com/poster.jpg'
        assert formatted['release_year'] == '2010'
        assert formatted['vote_average'] == 8.8
        assert formatted['vote_count'] == 25000
    
    def test_format_movie_data_missing_fields(self):
        """Test formatting movie data with missing fields."""
        raw_movie = {
            'id': 12345,
            'title': 'Inception',
            'overview': None,
            'poster_path': None,
            'release_date': None,
            'vote_average': None,
            'vote_count': None
        }
        
        formatted = format_movie_data(raw_movie, None)
        
        assert formatted['id'] == 12345
        assert formatted['title'] == 'Inception'
        assert formatted['overview'] == 'No overview available'
        assert formatted['poster_url'] is None
        assert formatted['release_year'] == 'Unknown'
        assert formatted['vote_average'] == 0.0
        assert formatted['vote_count'] == 0
    
    def test_format_movie_data_invalid_date(self):
        """Test formatting movie data with invalid date."""
        raw_movie = {
            'id': 12345,
            'title': 'Inception',
            'overview': 'A movie',
            'poster_path': '/test.jpg',
            'release_date': 'invalid-date',
            'vote_average': 8.5,
            'vote_count': 1000
        }
        
        formatted = format_movie_data(raw_movie, 'https://example.com/poster.jpg')
        
        assert formatted['release_year'] == 'invalid'
    
    def test_format_movie_data_long_overview(self):
        """Test formatting movie data with long overview."""
        long_overview = 'A' * 500  # Very long overview
        raw_movie = {
            'id': 12345,
            'title': 'Inception',
            'overview': long_overview,
            'poster_path': '/test.jpg',
            'release_date': '2010-07-16',
            'vote_average': 8.5,
            'vote_count': 1000
        }
        
        formatted = format_movie_data(raw_movie, 'https://example.com/poster.jpg')
        
        # Overview should be truncated
        assert len(formatted['overview']) <= 200
        assert formatted['overview'].endswith('...')


class TestMovieSearchIntegration:
    """Integration tests for movie search functionality."""
    
    def test_format_movie_data_integration(self):
        """Test format_movie_data function with real-world data."""
        # Test with complete movie data
        raw_movie = {
            'id': 12345,
            'title': 'Inception',
            'overview': 'A mind-bending thriller about dreams and reality',
            'poster_path': '/test_poster.jpg',
            'release_date': '2010-07-16',
            'vote_average': 8.8,
            'vote_count': 25000
        }
        
        formatted = format_movie_data(raw_movie, 'https://example.com/poster.jpg')
        
        assert formatted['id'] == 12345
        assert formatted['title'] == 'Inception'
        assert formatted['overview'] == 'A mind-bending thriller about dreams and reality'
        assert formatted['poster_url'] == 'https://example.com/poster.jpg'
        assert formatted['release_year'] == '2010'
        assert formatted['vote_average'] == 8.8
        assert formatted['vote_count'] == 25000
