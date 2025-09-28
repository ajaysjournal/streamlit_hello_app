"""TMDB API service for movie search functionality."""

import logging
from typing import Dict, List, Optional, Any
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout

# TMDB API Configuration
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_SEARCH_ENDPOINT = "/search/movie"
TMDB_CONFIG_ENDPOINT = "/configuration"


class TmdbService:
    """Service class for interacting with The Movie Database (TMDB) API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize TMDB service.
        
        Args:
            api_key: TMDB API key
        """
        self.api_key = api_key
        self.base_url = TMDB_BASE_URL
        self._config_cache = None
    
    def search_movies(self, query: str, page: int = 1) -> Dict[str, Any]:
        """
        Search for movies using TMDB API.
        
        Args:
            query: Search query string
            page: Page number for pagination
            
        Returns:
            Dictionary containing search results and metadata
        """
        if not self.api_key:
            return {
                'success': False,
                'error': 'API key is required'
            }
        
        if not query or not query.strip():
            return {
                'success': False,
                'error': 'Query cannot be empty'
            }
        
        try:
            url = f"{self.base_url}{TMDB_SEARCH_ENDPOINT}"
            params = {
                'api_key': self.api_key,
                'query': query.strip(),
                'page': page,
                'include_adult': False
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Format movie data
                movies = []
                for movie_data in data.get('results', []):
                    formatted_movie = self._format_movie_data(movie_data)
                    movies.append(formatted_movie)
                
                return {
                    'success': True,
                    'movies': movies,
                    'current_page': data.get('page', 1),
                    'total_pages': data.get('total_pages', 0),
                    'total_results': data.get('total_results', 0)
                }
            
            elif response.status_code == 401:
                return {
                    'success': False,
                    'error': 'Invalid API key'
                }
            
            else:
                error_data = response.json() if response.content else {}
                error_message = error_data.get('status_message', f'HTTP {response.status_code}')
                return {
                    'success': False,
                    'error': f'API error: {error_message}'
                }
                
        except (ConnectionError, Timeout) as e:
            logging.error(f"TMDB API connection error: {e}")
            return {
                'success': False,
                'error': f'Connection error: {str(e)}'
            }
        except RequestException as e:
            logging.error(f"TMDB API request error: {e}")
            return {
                'success': False,
                'error': f'Request error: {str(e)}'
            }
        except Exception as e:
            logging.error(f"Unexpected error in TMDB search: {e}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def get_movie_poster_url(self, poster_path: Optional[str], size: str = 'w500') -> Optional[str]:
        """
        Get full URL for movie poster image.
        
        Args:
            poster_path: Poster path from TMDB API
            size: Image size (w92, w154, w185, w342, w500, w780, original)
            
        Returns:
            Full poster URL or None if no poster path
        """
        if not poster_path:
            return None
        
        try:
            # Get configuration if not cached
            if not self._config_cache:
                self._config_cache = self._get_configuration()
            
            if not self._config_cache:
                return None
            
            base_url = self._config_cache.get('images', {}).get('base_url')
            if not base_url:
                return None
            
            return f"{base_url}{size}{poster_path}"
            
        except Exception as e:
            logging.error(f"Error getting poster URL: {e}")
            return None
    
    def _get_configuration(self) -> Optional[Dict[str, Any]]:
        """
        Get TMDB API configuration.
        
        Returns:
            Configuration dictionary or None if failed
        """
        if not self.api_key:
            return None
        
        try:
            url = f"{self.base_url}{TMDB_CONFIG_ENDPOINT}"
            params = {'api_key': self.api_key}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to get TMDB configuration: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Error getting TMDB configuration: {e}")
            return None
    
    def _format_movie_data(self, movie_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format raw movie data from TMDB API.
        
        Args:
            movie_data: Raw movie data from API
            
        Returns:
            Formatted movie data
        """
        # Get poster URL
        poster_url = self.get_movie_poster_url(movie_data.get('poster_path'))
        
        # Extract release year
        release_date = movie_data.get('release_date', '')
        release_year = 'Unknown'
        if release_date:
            try:
                release_year = release_date.split('-')[0]
            except (IndexError, AttributeError):
                release_year = 'Unknown'
        
        # Format overview (truncate if too long)
        overview = movie_data.get('overview', '')
        if not overview:
            overview = 'No overview available'
        elif len(overview) > 200:
            overview = overview[:200] + '...'
        
        return {
            'id': movie_data.get('id'),
            'title': movie_data.get('title', 'Unknown Title'),
            'overview': overview,
            'poster_url': poster_url,
            'release_year': release_year,
            'vote_average': movie_data.get('vote_average', 0.0),
            'vote_count': movie_data.get('vote_count', 0)
        }
