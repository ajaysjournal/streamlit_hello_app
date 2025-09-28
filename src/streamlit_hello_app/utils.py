"""Utility functions for the Streamlit Hello App."""

import logging
import os
from pathlib import Path
from typing import Optional
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout

from dotenv import load_dotenv


def setup_logging(level: str = "INFO") -> None:
    """
    Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def load_environment(env_file: Optional[Path] = None) -> None:
    """
    Load environment variables from .env file.
    
    Args:
        env_file: Optional path to .env file
    """
    if env_file and env_file.exists():
        load_dotenv(env_file)
    else:
        # Try to load from default locations
        env_paths = [
            Path(".env"),
            Path(".env.local"),
            Path(".env.development"),
        ]
        
        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path)
                break


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path to the project root directory
    """
    return Path(__file__).parent.parent.parent


def ensure_directory(path: Path) -> None:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        path: Directory path to ensure exists
    """
    path.mkdir(parents=True, exist_ok=True)


# TMDB API Constants
TMDB_API_KEY_VALID = "valid"
TMDB_API_KEY_INVALID = "invalid"
TMDB_API_KEY_ERROR = "error"


def get_tmdb_api_key() -> Optional[str]:
    """
    Get TMDB API key from environment variable or user input.
    
    Returns:
        API key string if available, None otherwise
    """
    # First try to get from environment variable
    api_key = os.getenv('TMDB_API_KEY')
    
    if api_key:
        return api_key
    
    # If not in environment, ask user for input
    try:
        import streamlit as st
        api_key = st.text_input(
            "Enter your TMDB API key:",
            type="password",
            help="Get your API key from https://www.themoviedb.org/settings/api"
        )
        return api_key if api_key else None
    except ImportError:
        # If streamlit is not available (e.g., in tests), return None
        return None


def validate_tmdb_api_key(api_key: Optional[str]) -> str:
    """
    Validate TMDB API key by making a test request.
    
    Args:
        api_key: API key to validate
        
    Returns:
        Validation result: 'valid', 'invalid', or 'error'
    """
    if not api_key:
        return TMDB_API_KEY_ERROR
    
    try:
        # Make a test request to TMDB API
        url = "https://api.themoviedb.org/3/authentication"
        params = {"api_key": api_key}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            # Try to parse JSON to ensure it's a valid response
            try:
                response.json()
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
