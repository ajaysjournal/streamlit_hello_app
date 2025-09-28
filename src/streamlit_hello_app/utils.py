"""Utility functions for the Streamlit Hello App."""

import logging
import os
from pathlib import Path
from typing import Optional

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
