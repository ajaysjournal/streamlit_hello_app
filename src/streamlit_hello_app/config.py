"""Configuration management for the Streamlit Hello App."""

from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict
import tomllib


class AppConfig(BaseModel):
    """Application configuration model."""
    
    app_name: str = Field(default="Streamlit Hello App", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    theme: Dict[str, Any] = Field(
        default_factory=lambda: {
            "primary_color": "#FF6B6B",
            "background_color": "#FFFFFF",
            "secondary_background_color": "#F0F2F6",
            "text_color": "#404040",
        },
        description="UI theme configuration"
    )
    
    model_config = ConfigDict(env_prefix="STREAMLIT_")


def load_config(config_path: Optional[Path] = None) -> AppConfig:
    """
    Load configuration from TOML file or environment variables.
    
    Args:
        config_path: Optional path to TOML configuration file
        
    Returns:
        AppConfig instance with loaded configuration
    """
    config_data: Dict[str, Any] = {}
    
    # Try to load from TOML file
    if config_path and config_path.exists():
        with open(config_path, "rb") as f:
            config_data = tomllib.load(f)
    
    # Create config instance
    config = AppConfig(**config_data)
    
    return config


# Default configuration instance
default_config = load_config()
