"""
Streamlit Hello App - A modern Python web application package.

This package provides a Streamlit-based web application with modern Python practices,
including type hints, configuration management, and clean architecture.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .config import AppConfig
from .utils import setup_logging, load_environment

__all__ = [
    "AppConfig",
    "setup_logging", 
    "load_environment",
    "__version__",
    "__author__",
    "__email__",
]
