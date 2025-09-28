"""Streamlit UI components for the Hello App."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any

from streamlit_hello_app.config import AppConfig


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
    page = st.sidebar.selectbox(
        "Select a page:",
        pages,
        index=pages.index(st.session_state.get("page", "Dashboard"))
    )
    
    # Update session state
    st.session_state.page = page
    
    # Add some sidebar content
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛️ Settings")
    
    # Theme selector
    theme = st.sidebar.selectbox(
        "Theme:",
        ["Light", "Dark", "Auto"],
        index=0
    )
    
    # Debug mode toggle
    debug_mode = st.sidebar.checkbox("Debug Mode", value=False)
    
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
        
        fig = px.line(df, x='Date', y='Value', title='Sample Time Series')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Sample Pie Chart")
        
        # Generate sample data
        categories = ['Category A', 'Category B', 'Category C', 'Category D']
        values = np.random.randint(10, 100, len(categories))
        
        fig = px.pie(values=values, names=categories, title='Sample Distribution')
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
                        fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    hist_col = st.selectbox("Histogram column:", numeric_columns)
                    if hist_col:
                        fig = px.histogram(df, x=hist_col, title=f"Distribution of {hist_col}")
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
            fig = px.bar(sample_df, x='Name', y='Salary', title='Salary by Name')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(sample_df, x='Age', y='Salary', hover_data=['City'], 
                           title='Age vs Salary')
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
