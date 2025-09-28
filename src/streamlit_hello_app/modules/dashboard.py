"""Dashboard page component for Streamlit Hello App."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_hello_app.components import get_plotly_dark_theme


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
        theme_config = get_plotly_dark_theme()
        
        fig = px.line(df, x='Date', y='Value', title='Sample Time Series')
        fig.update_layout(**theme_config["layout"])
        st.plotly_chart(fig, config={'displayModeBar': False})
    
    with col2:
        st.subheader("🥧 Sample Pie Chart")
        
        # Generate sample data
        categories = ['Category A', 'Category B', 'Category C', 'Category D']
        values = np.random.randint(10, 100, len(categories))
        
        # Get current theme for chart styling
        theme_config = get_plotly_dark_theme()
        
        fig = px.pie(values=values, names=categories, title='Sample Distribution')
        fig.update_layout(**theme_config["layout"])
        st.plotly_chart(fig, config={'displayModeBar': False})
    
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
