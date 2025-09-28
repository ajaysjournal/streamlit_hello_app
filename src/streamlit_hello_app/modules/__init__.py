"""Pages module for Streamlit Hello App.

This module contains all the page components organized by functionality.
"""

from .dashboard import render_dashboard
from .data_explorer import render_data_explorer
from .compound_interest import render_compound_interest_calculator, calculate_compound_interest
from .about import render_about

__all__ = [
    'render_dashboard',
    'render_data_explorer', 
    'render_compound_interest_calculator',
    'calculate_compound_interest',
    'render_about'
]
