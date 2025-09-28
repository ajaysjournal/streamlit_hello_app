"""About page component for Streamlit Hello App."""

import streamlit as st
from streamlit_hello_app.config import AppConfig


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
    - 💰 **Compound Interest Calculator** for financial planning
    
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
    │   ├── components.py
    │   └── pages/
    │       ├── __init__.py
    │       ├── dashboard.py
    │       ├── data_explorer.py
    │       ├── compound_interest.py
    │       └── about.py
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
