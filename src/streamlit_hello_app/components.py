"""Streamlit UI components for the Hello App."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any

from streamlit_hello_app.config import AppConfig


def get_plotly_theme_config(theme: str) -> dict:
    """
    Get Plotly theme configuration based on the selected theme.
    
    Args:
        theme: Theme name ("Light", "Dark", or "Auto")
    
    Returns:
        Dictionary with Plotly theme configuration
    """
    if theme == "Dark":
        return {
            "layout": {
                "paper_bgcolor": "#0E1117",
                "plot_bgcolor": "#0E1117",
                "font": {"color": "#FAFAFA"},
                "xaxis": {
                    "gridcolor": "#404040",
                    "color": "#FAFAFA"
                },
                "yaxis": {
                    "gridcolor": "#404040", 
                    "color": "#FAFAFA"
                }
            }
        }
    elif theme == "Auto":
        # For auto theme, detect system preference and use appropriate colors
        # This is a simplified approach - in a real app you might want to use JavaScript detection
        import os
        # Check if we're in a dark environment (this is a basic heuristic)
        # In a real implementation, you'd use JavaScript to detect prefers-color-scheme
        return {
            "layout": {
                "paper_bgcolor": "#0E1117",  # Default to dark for auto
                "plot_bgcolor": "#0E1117",
                "font": {"color": "#FAFAFA"},
                "xaxis": {
                    "gridcolor": "#404040",
                    "color": "#FAFAFA"
                },
                "yaxis": {
                    "gridcolor": "#404040",
                    "color": "#FAFAFA"
                }
            }
        }
    else:  # Light theme
        return {
            "layout": {
                "paper_bgcolor": "#FFFFFF",
                "plot_bgcolor": "#FFFFFF", 
                "font": {"color": "#262730"},
                "xaxis": {
                    "gridcolor": "#E5E5E5",
                    "color": "#262730"
                },
                "yaxis": {
                    "gridcolor": "#E5E5E5",
                    "color": "#262730"
                }
            }
        }


def apply_theme(theme: str) -> None:
    """
    Apply the selected theme to the Streamlit app.
    
    Args:
        theme: Theme name ("Light", "Dark", or "Auto")
    """
    if theme == "Light":
        st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF !important;
            color: #262730 !important;
        }
        .stApp > div {
            background-color: #FFFFFF !important;
            color: #262730 !important;
        }
        .stApp > div > div {
            background-color: #FFFFFF !important;
            color: #262730 !important;
        }
        .main .block-container {
            background-color: #FFFFFF !important;
            color: #262730 !important;
        }
        .main .block-container > div {
            background-color: #FFFFFF !important;
            color: #262730 !important;
        }
        .stSidebar {
            background-color: #F0F2F6 !important;
        }
        .stSelectbox > div > div {
            background-color: #FFFFFF !important;
            color: #262730 !important;
        }
        .stMetric {
            background-color: #FFFFFF !important;
            color: #262730 !important;
        }
        .stDataFrame {
            background-color: #FFFFFF !important;
            color: #262730 !important;
        }
        .stTextInput > div > div > input {
            background-color: #FFFFFF !important;
            color: #262730 !important;
        }
        .stTextArea > div > div > textarea {
            background-color: #FFFFFF !important;
            color: #262730 !important;
        }
        
        /* Force all main content elements to light mode */
        .main .block-container h1,
        .main .block-container h2,
        .main .block-container h3,
        .main .block-container h4,
        .main .block-container h5,
        .main .block-container h6,
        .main .block-container p,
        .main .block-container div,
        .main .block-container span,
        .main .block-container label {
            color: #262730 !important;
        }
        
        /* Force all text elements to dark color in light mode */
        h1, h2, h3, h4, h5, h6, p, div, span, label {
            color: #262730 !important;
        }
        
        /* Orange dropdown font in light mode */
        .stSelectbox > div > div {
            color: #FF6B6B !important;
        }
        .stSelectbox > div > div > div {
            color: #FF6B6B !important;
        }
        .stSelectbox > div > div > div > div {
            color: #FF6B6B !important;
        }
        </style>
        """, unsafe_allow_html=True)
    elif theme == "Dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
        }
        .stApp > div {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
        }
        .stApp > div > div {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
        }
        .main .block-container {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
        }
        .main .block-container > div {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
        }
        .stSidebar {
            background-color: #262730 !important;
        }
        .stSidebar * {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSidebar *:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSidebar *:focus {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSidebar *:active {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSidebar .stSelectbox > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSidebar .stSelectbox label {
            color: #FAFAFA !important;
        }
        .stSidebar .stCheckbox label {
            color: #FAFAFA !important;
        }
        .stSidebar .stCheckbox > div > div {
            background-color: #262730 !important;
        }
        .stSidebar .stMarkdown {
            color: #FAFAFA !important;
        }
        .stSidebar .stMarkdown p {
            color: #FAFAFA !important;
        }
        .stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3, 
        .stSidebar .stMarkdown h4, .stSidebar .stMarkdown h5, .stSidebar .stMarkdown h6 {
            color: #FAFAFA !important;
        }
        .stSidebar .stButton > button {
            background-color: #404040 !important;
            color: #FAFAFA !important;
            border: 1px solid #606060 !important;
        }
        .stSidebar .stButton > button:hover {
            background-color: #505050 !important;
            color: #FAFAFA !important;
        }
        .stSidebar .stSelectbox > div > div > div {
            color: #FAFAFA !important;
        }
        .stSidebar .stSelectbox > div > div > div > div {
            color: #FAFAFA !important;
        }
        
        /* Fix dropdown menu styling in dark mode */
        .stSelectbox > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional dropdown menu styling */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target the actual dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional targeting for dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target any remaining dropdown elements */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target the actual dropdown menu container */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target dropdown menu items specifically */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional targeting for dropdown menu items */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target dropdown menu text elements */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* General dropdown menu targeting */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target any remaining dropdown elements with more general selectors */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional general targeting for dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional general targeting for dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target any remaining dropdown elements with more general selectors */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional general targeting for dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional general targeting for dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target any remaining dropdown elements with more general selectors */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional general targeting for dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional general targeting for dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target any remaining dropdown elements with more general selectors */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional general targeting for dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional general targeting for dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target any remaining dropdown elements with more general selectors */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional general targeting for dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional general targeting for dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target any remaining dropdown elements with more general selectors */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional general targeting for dropdown menu */
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Use more general selectors for dropdown menu */
        .stSelectbox [data-baseweb="select"] {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] * {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] *:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target dropdown menu items more broadly */
        .stSelectbox [data-baseweb="select"] > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional CSS targeting for dropdown menu */
        .stSelectbox [data-baseweb="select"] [role="listbox"] {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="option"] {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="option"]:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="option"]:focus {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="option"]:active {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional CSS targeting for dropdown menu */
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional CSS targeting for dropdown menu */
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        
        /* Force all dropdown elements to dark mode */
        .stSelectbox * {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox *:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox *:focus {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox *:active {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target any element with white background in selectbox */
        .stSelectbox [style*="background-color: white"],
        .stSelectbox [style*="background-color: #ffffff"],
        .stSelectbox [style*="background-color: #FFFFFF"] {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        
        /* Target any element with black text in selectbox */
        .stSelectbox [style*="color: black"],
        .stSelectbox [style*="color: #000000"],
        .stSelectbox [style*="color: #000"] {
            color: #FAFAFA !important;
        }
        
        /* Force all dropdown elements to dark mode */
        .stSelectbox [data-baseweb="select"] * {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] *:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] *:focus {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] *:active {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target dropdown menu container */
        .stSelectbox [data-baseweb="select"] [role="listbox"] {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] * {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] *:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] *:focus {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] *:active {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Additional aggressive CSS targeting */
        .stSelectbox [data-baseweb="select"] [role="listbox"] * {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] *:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] *:focus {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] *:active {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        
        /* Target any remaining dropdown elements */
        .stSelectbox [data-baseweb="select"] [role="listbox"] * * {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] * *:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] * *:focus {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox [data-baseweb="select"] [role="listbox"] * *:active {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stMetric {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stDataFrame {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stTextInput > div > div > input {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stTextArea > div > div > textarea {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .stSlider > div > div > div > div {
            background-color: #262730 !important;
        }
        .stCheckbox > div > div {
            background-color: #262730 !important;
        }
        .stRadio > div > div {
            background-color: #262730 !important;
        }
        
        /* Fix text visibility in dark mode */
        h1, h2, h3, h4, h5, h6 {
            color: #FAFAFA !important;
        }
        p, div, span, label {
            color: #FAFAFA !important;
        }
        .stMarkdown {
            color: #FAFAFA !important;
        }
        .stMarkdown p {
            color: #FAFAFA !important;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #FAFAFA !important;
        }
        .stButton > button {
            background-color: #262730 !important;
            color: #FAFAFA !important;
            border: 1px solid #404040 !important;
        }
        .stButton > button:hover {
            background-color: #404040 !important;
            color: #FAFAFA !important;
        }
        .stSelectbox label {
            color: #FAFAFA !important;
        }
        .stSlider label {
            color: #FAFAFA !important;
        }
        .stCheckbox label {
            color: #FAFAFA !important;
        }
        .stRadio label {
            color: #FAFAFA !important;
        }
        .stFileUploader label {
            color: #FAFAFA !important;
        }
        .stNumberInput label {
            color: #FAFAFA !important;
        }
        .stTextInput label {
            color: #FAFAFA !important;
        }
        .stTextArea label {
            color: #FAFAFA !important;
        }
        .stDateInput label {
            color: #FAFAFA !important;
        }
        .stTimeInput label {
            color: #FAFAFA !important;
        }
        .stSelectbox > div > div > div {
            color: #FAFAFA !important;
        }
        .stMultiSelect label {
            color: #FAFAFA !important;
        }
        .stMultiSelect > div > div > div {
            color: #FAFAFA !important;
        }
        
        /* Additional styling for main content area */
        .main .block-container {
            color: #FAFAFA !important;
        }
        .main .block-container h1, .main .block-container h2, .main .block-container h3, 
        .main .block-container h4, .main .block-container h5, .main .block-container h6 {
            color: #FAFAFA !important;
        }
        .main .block-container p, .main .block-container div, .main .block-container span {
            color: #FAFAFA !important;
        }
        .main .block-container .stMarkdown {
            color: #FAFAFA !important;
        }
        .main .block-container .stMarkdown p {
            color: #FAFAFA !important;
        }
        .main .block-container .stMarkdown h1, .main .block-container .stMarkdown h2, 
        .main .block-container .stMarkdown h3, .main .block-container .stMarkdown h4, 
        .main .block-container .stMarkdown h5, .main .block-container .stMarkdown h6 {
            color: #FAFAFA !important;
        }
        
        /* Force all main content elements to dark mode */
        .main .block-container h1,
        .main .block-container h2,
        .main .block-container h3,
        .main .block-container h4,
        .main .block-container h5,
        .main .block-container h6,
        .main .block-container p,
        .main .block-container div,
        .main .block-container span,
        .main .block-container label {
            color: #FAFAFA !important;
        }
        
        /* Force all elements with white background to dark */
        *[style*="background-color: white"],
        *[style*="background-color: #ffffff"],
        *[style*="background-color: #FFFFFF"],
        *[style*="background-color: rgb(255, 255, 255)"] {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
        }
        
        /* Force all elements with light gray background to dark */
        *[style*="background-color: #F0F2F6"],
        *[style*="background-color: #f0f2f6"],
        *[style*="background-color: rgb(240, 242, 246)"] {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
        }
        
        /* Orange dropdown font in dark mode */
        .stSelectbox > div > div {
            color: #FF6B6B !important;
        }
        .stSelectbox > div > div > div {
            color: #FF6B6B !important;
        }
        .stSelectbox > div > div > div > div {
            color: #FF6B6B !important;
        }
        </style>
        """, unsafe_allow_html=True)
    elif theme == "Auto":
        # Auto theme - use system preference
        st.markdown("""
        <style>
        @media (prefers-color-scheme: dark) {
            .stApp {
                background-color: #0E1117 !important;
                color: #FAFAFA !important;
            }
            .stSidebar {
                background-color: #262730 !important;
            }
            .stSidebar .stSelectbox > div > div {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            .stSidebar .stSelectbox label {
                color: #FAFAFA !important;
            }
            .stSidebar .stCheckbox label {
                color: #FAFAFA !important;
            }
            .stSidebar .stCheckbox > div > div {
                background-color: #262730 !important;
            }
            .stSidebar .stMarkdown {
                color: #FAFAFA !important;
            }
            .stSidebar .stMarkdown p {
                color: #FAFAFA !important;
            }
            .stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3, 
            .stSidebar .stMarkdown h4, .stSidebar .stMarkdown h5, .stSidebar .stMarkdown h6 {
                color: #FAFAFA !important;
            }
            .stSidebar .stButton > button {
                background-color: #404040 !important;
                color: #FAFAFA !important;
                border: 1px solid #606060 !important;
            }
            .stSidebar .stButton > button:hover {
                background-color: #505050 !important;
                color: #FAFAFA !important;
            }
            .stSelectbox > div > div {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            
            /* Fix dropdown menu styling in dark mode */
            .stSelectbox > div > div > div {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            .stSelectbox > div > div > div > div {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            .stSelectbox > div > div > div > div:hover {
                background-color: #404040 !important;
                color: #FAFAFA !important;
            }
            .stSelectbox > div > div > div > div[data-baseweb="select"] {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            .stSelectbox > div > div > div > div[data-baseweb="select"] > div {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            .stSelectbox > div > div > div > div[data-baseweb="select"] > div:hover {
                background-color: #404040 !important;
                color: #FAFAFA !important;
            }
            .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            .stSelectbox > div > div > div > div[data-baseweb="select"] > div > div:hover {
                background-color: #404040 !important;
                color: #FAFAFA !important;
            }
            .stMetric {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            .stDataFrame {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            
            /* Fix text visibility in dark mode */
            h1, h2, h3, h4, h5, h6 {
                color: #FAFAFA !important;
            }
            p, div, span, label {
                color: #FAFAFA !important;
            }
            .stMarkdown {
                color: #FAFAFA !important;
            }
            .stMarkdown p {
                color: #FAFAFA !important;
            }
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
                color: #FAFAFA !important;
            }
            .stButton > button {
                background-color: #262730 !important;
                color: #FAFAFA !important;
                border: 1px solid #404040 !important;
            }
            .stButton > button:hover {
                background-color: #404040 !important;
                color: #FAFAFA !important;
            }
            .stSelectbox label, .stSlider label, .stCheckbox label, .stRadio label, 
            .stFileUploader label, .stNumberInput label, .stTextInput label, 
            .stTextArea label, .stDateInput label, .stTimeInput label, 
            .stMultiSelect label {
                color: #FAFAFA !important;
            }
            .stSelectbox > div > div > div, .stMultiSelect > div > div > div {
                color: #FAFAFA !important;
            }
        }
        @media (prefers-color-scheme: light) {
            .stApp {
                background-color: #FFFFFF !important;
                color: #262730 !important;
            }
            .stSidebar {
                background-color: #F0F2F6 !important;
            }
            .stSelectbox > div > div {
                background-color: #FFFFFF !important;
                color: #262730 !important;
            }
            .stMetric {
                background-color: #FFFFFF !important;
                color: #262730 !important;
            }
            .stDataFrame {
                background-color: #FFFFFF !important;
                color: #262730 !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)


def render_header(config: AppConfig) -> None:
    """
    Render the application header.
    
    Args:
        config: Application configuration
    """
    st.title("🚀 Streamlit Hello App")
    st.markdown(f"**Version:** {config.app_version}")
    
    # Add some styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar() -> str:
    """
    Render the sidebar navigation.
    
    Returns:
        Selected page name
    """
    st.sidebar.title("📋 Navigation")
    
    pages = ["Dashboard", "Data Explorer", "About"]
    current_page = st.session_state.get("page", "Dashboard")
    
    # Initialize page selector in session state
    if "page_selector" not in st.session_state:
        st.session_state.page_selector = current_page
    
    page = st.sidebar.selectbox(
        "Select a page:",
        pages,
        index=pages.index(current_page),
        key="page_selector"
    )
    
    # Update session state
    st.session_state.page = page
    
    # Add some sidebar content
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛️ Settings")
    
    # Theme selector with proper functionality
    theme_options = ["Light", "Dark", "Auto"]
    current_theme = st.session_state.get("theme", "Dark")
    
    # Initialize theme selector in session state
    if "theme_selector" not in st.session_state:
        st.session_state.theme_selector = current_theme
    
    theme = st.sidebar.selectbox(
        "Theme:",
        theme_options,
        index=theme_options.index(current_theme),
        key="theme_selector"
    )
    
    # Update session state and apply theme
    if theme != current_theme:
        st.session_state.theme = theme
        apply_theme(theme)
        st.rerun()  # Force rerun to apply theme changes
    
    # Debug mode toggle
    # Initialize debug mode in session state
    if "debug_mode" not in st.session_state:
        st.session_state.debug_mode = False
    
    debug_mode = st.sidebar.checkbox("Debug Mode", value=st.session_state.debug_mode, key="debug_mode")
    
    return page


def render_dashboard() -> None:
    """Render the main dashboard page."""
    st.header("📊 Dashboard")
    
    # Create some sample data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Users",
            value="1,234",
            delta="12%"
        )
    
    with col2:
        st.metric(
            label="Active Sessions",
            value="567",
            delta="8%"
        )
    
    with col3:
        st.metric(
            label="Page Views",
            value="9,876",
            delta="-3%"
        )
    
    with col4:
        st.metric(
            label="Conversion Rate",
            value="3.2%",
            delta="1.5%"
        )
    
    # Charts section
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Sample Line Chart")
        
        # Generate sample data
        dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
        values = np.cumsum(np.random.randn(31)) + 100
        
        df = pd.DataFrame({
            'Date': dates,
            'Value': values
        })
        
        # Get current theme for chart styling
        current_theme = st.session_state.get("theme", "Light")
        theme_config = get_plotly_theme_config(current_theme)
        
        fig = px.line(df, x='Date', y='Value', title='Sample Time Series')
        fig.update_layout(**theme_config["layout"])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Sample Pie Chart")
        
        # Generate sample data
        categories = ['Category A', 'Category B', 'Category C', 'Category D']
        values = np.random.randint(10, 100, len(categories))
        
        # Get current theme for chart styling
        current_theme = st.session_state.get("theme", "Light")
        theme_config = get_plotly_theme_config(current_theme)
        
        fig = px.pie(values=values, names=categories, title='Sample Distribution')
        fig.update_layout(**theme_config["layout"])
        st.plotly_chart(fig, use_container_width=True)
    
    # Interactive elements
    st.markdown("---")
    st.subheader("🎮 Interactive Elements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Slider
        slider_value = st.slider(
            "Select a value:",
            min_value=0,
            max_value=100,
            value=50,
            step=5
        )
        st.write(f"Selected value: {slider_value}")
        
        # Selectbox
        option = st.selectbox(
            "Choose an option:",
            ["Option 1", "Option 2", "Option 3", "Option 4"]
        )
        st.write(f"Selected option: {option}")
    
    with col2:
        # Checkboxes
        st.write("Select features:")
        feature1 = st.checkbox("Feature 1", value=True)
        feature2 = st.checkbox("Feature 2", value=False)
        feature3 = st.checkbox("Feature 3", value=True)
        
        # Radio buttons
        color = st.radio(
            "Choose a color:",
            ["Red", "Green", "Blue", "Yellow"]
        )
        st.write(f"Selected color: {color}")


def render_data_explorer() -> None:
    """Render the data explorer page."""
    st.header("🔍 Data Explorer")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload a CSV file to explore its data"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10))
            
            st.subheader("📊 Data Summary")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Dataset Info:**")
                st.write(f"- Rows: {len(df)}")
                st.write(f"- Columns: {len(df.columns)}")
                st.write(f"- Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
            
            with col2:
                st.write("**Column Types:**")
                st.dataframe(df.dtypes.to_frame('Type'))
            
            # Column selector for visualization
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_columns:
                st.subheader("📈 Data Visualization")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("X-axis:", numeric_columns)
                    y_col = st.selectbox("Y-axis:", numeric_columns)
                    
                    if x_col and y_col and x_col != y_col:
                        # Get current theme for chart styling
                        current_theme = st.session_state.get("theme", "Light")
                        theme_config = get_plotly_theme_config(current_theme)
                        
                        fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
                        fig.update_layout(**theme_config["layout"])
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    hist_col = st.selectbox("Histogram column:", numeric_columns)
                    if hist_col:
                        # Get current theme for chart styling
                        current_theme = st.session_state.get("theme", "Light")
                        theme_config = get_plotly_theme_config(current_theme)
                        
                        fig = px.histogram(df, x=hist_col, title=f"Distribution of {hist_col}")
                        fig.update_layout(**theme_config["layout"])
                        st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    else:
        st.info("👆 Please upload a CSV file to explore data")
        
        # Show sample data
        st.subheader("🎯 Sample Data")
        sample_data = {
            'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'Age': [25, 30, 35, 28, 32],
            'City': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney'],
            'Salary': [50000, 60000, 70000, 55000, 65000]
        }
        sample_df = pd.DataFrame(sample_data)
        
        st.dataframe(sample_df)
        
        # Interactive visualization of sample data
        st.subheader("📊 Sample Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Get current theme for chart styling
            current_theme = st.session_state.get("theme", "Light")
            theme_config = get_plotly_theme_config(current_theme)
            
            fig = px.bar(sample_df, x='Name', y='Salary', title='Salary by Name')
            fig.update_layout(**theme_config["layout"])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Get current theme for chart styling
            current_theme = st.session_state.get("theme", "Light")
            theme_config = get_plotly_theme_config(current_theme)
            
            fig = px.scatter(sample_df, x='Age', y='Salary', hover_data=['City'], 
                           title='Age vs Salary')
            fig.update_layout(**theme_config["layout"])
            st.plotly_chart(fig, use_container_width=True)


def render_about(config: AppConfig) -> None:
    """
    Render the about page.
    
    Args:
        config: Application configuration
    """
    st.header("ℹ️ About")
    
    st.markdown(f"""
    ## {config.app_name}
    
    **Version:** {config.app_version}
    
    This is a modern Python web application built with Streamlit, featuring:
    
    - 🐍 **Python 3.12+** with modern type hints
    - 📦 **PyTOML** for configuration management
    - 🎨 **Streamlit** for the web interface
    - 📊 **Interactive visualizations** with Plotly
    - 🔧 **Clean architecture** with Pydantic models
    - 📈 **Data exploration** capabilities
    
    ### 🛠️ Technology Stack
    
    - **Backend:** Python 3.12+
    - **Web Framework:** Streamlit
    - **Data Processing:** Pandas, NumPy
    - **Visualizations:** Plotly
    - **Configuration:** PyTOML
    - **Validation:** Pydantic
    - **Environment:** python-dotenv
    
    ### 📁 Project Structure
    
    ```
    streamlit_hello_app/
    ├── src/streamlit_hello_app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── config.py
    │   ├── utils.py
    │   └── components.py
    ├── pyproject.toml
    ├── README.md
    └── .gitignore
    ```
    
    ### 🚀 Getting Started
    
    1. Install dependencies: `pip install -e .`
    2. Run the app: `streamlit run src/streamlit_hello_app/main.py`
    3. Open your browser to the provided URL
    
    ### 📝 License
    
    This project is licensed under the MIT License.
    """)
    
    # Add contact information
    st.markdown("---")
    st.markdown("### 📧 Contact")
    st.markdown(f"**Author:** {config.__class__.__name__}")
    st.markdown("**Email:** your.email@example.com")
    st.markdown("**GitHub:** https://github.com/yourusername/streamlit-hello-app")
