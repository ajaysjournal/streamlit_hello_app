"""Chat interface module with OpenAI integration and file upload functionality."""

import streamlit as st
import base64
import io
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

from streamlit_hello_app.utils import get_openai_api_key, validate_openai_api_key, OPENAI_API_KEY_VALID
from streamlit_hello_app.modules.openai_service import OpenAIService


def render_chat_interface() -> None:
    """
    Render the main chat interface with file upload functionality.
    """
    st.title("🤖 OpenAI Chat Assistant")
    st.markdown("Chat with OpenAI's GPT models. Upload files or images to get help with your content.")
    
    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    
    # API Key Management
    api_key = get_openai_api_key()
    
    if not api_key:
        st.error("Please provide your OpenAI API key to use the chat feature.")
        st.info("You can get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)")
        return
    
    # Validate API key
    validation_result = validate_openai_api_key(api_key)
    if validation_result != OPENAI_API_KEY_VALID:
        if validation_result == "invalid":
            st.error("Invalid API key. Please check your key and try again.")
        else:
            st.error("Error validating API key. Please check your connection and try again.")
        return
    
    # Initialize OpenAI service
    openai_service = OpenAIService(api_key)
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Chat Settings")
        
        # Model selection
        models_result = openai_service.get_available_models()
        if models_result['success']:
            available_models = [model['id'] for model in models_result['models']]
            # Filter for common chat models
            chat_models = [m for m in available_models if m.startswith(('gpt-3.5', 'gpt-4'))]
            if not chat_models:
                chat_models = available_models[:5]  # Show first 5 models if no common ones found
        else:
            chat_models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
        
        selected_model = st.selectbox(
            "Choose Model:",
            chat_models,
            index=0 if "gpt-3.5-turbo" in chat_models else 0
        )
        
        # Temperature setting
        temperature = st.slider(
            "Temperature (Creativity):",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Lower values make responses more focused, higher values more creative."
        )
        
        # Max tokens setting
        max_tokens = st.number_input(
            "Max Tokens:",
            min_value=50,
            max_value=4000,
            value=1000,
            step=50,
            help="Maximum number of tokens in the response."
        )
        
        # System message
        system_message = st.text_area(
            "System Message (Optional):",
            value="You are a helpful AI assistant. Be concise and helpful in your responses.",
            help="This sets the context for how the AI should behave."
        )
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.uploaded_files = []
            st.rerun()
    
    # File upload section
    st.subheader("📁 Upload Files")
    
    uploaded_files = st.file_uploader(
        "Choose files to upload:",
        type=['txt', 'pdf', 'docx', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'json'],
        accept_multiple_files=True,
        help="Upload text files, images, or documents to get help with their content."
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file not in st.session_state.uploaded_files:
                st.session_state.uploaded_files.append(uploaded_file)
        
        # Display uploaded files
        st.write("**Uploaded Files:**")
        for i, file in enumerate(st.session_state.uploaded_files):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"📄 {file.name} ({file.size} bytes)")
            with col2:
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.uploaded_files.pop(i)
                    st.rerun()
    
    # Chat input
    st.subheader("💬 Chat")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            # Display file content if available
            if "files" in message and message["files"]:
                st.write("**Attached files:**")
                for file_info in message["files"]:
                    st.write(f"📄 {file_info['name']}")
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to history
        user_message = {
            "role": "user",
            "content": user_input,
            "files": []
        }
        
        # Process uploaded files
        if st.session_state.uploaded_files:
            for file in st.session_state.uploaded_files:
                file_content = _process_uploaded_file(file)
                if file_content:
                    user_message["files"].append({
                        "name": file.name,
                        "content": file_content,
                        "type": file.type
                    })
        
        st.session_state.chat_history.append(user_message)
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
            if user_message["files"]:
                st.write("**Attached files:**")
                for file_info in user_message["files"]:
                    st.write(f"📄 {file_info['name']}")
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Prepare conversation for API
                conversation = []
                
                # Add system message if provided
                if system_message.strip():
                    conversation.append({
                        "role": "system",
                        "content": system_message.strip()
                    })
                
                # Add file content to user message if files are uploaded
                full_user_message = user_input
                if user_message["files"]:
                    file_context = "\n\n**Uploaded files content:**\n"
                    for file_info in user_message["files"]:
                        file_context += f"\n--- {file_info['name']} ---\n"
                        file_context += file_info['content']
                        file_context += "\n"
                    full_user_message += file_context
                
                # Add conversation history
                for msg in st.session_state.chat_history[-10:]:  # Keep last 10 messages for context
                    if msg["role"] == "user":
                        # Include file content in user messages
                        if msg.get("files"):
                            file_context = "\n\n**Uploaded files content:**\n"
                            for file_info in msg["files"]:
                                file_context += f"\n--- {file_info['name']} ---\n"
                                file_context += file_info['content']
                                file_context += "\n"
                            conversation.append({
                                "role": "user",
                                "content": msg["content"] + file_context
                            })
                        else:
                            conversation.append({
                                "role": "user",
                                "content": msg["content"]
                            })
                    elif msg["role"] == "assistant":
                        conversation.append({
                            "role": "assistant",
                            "content": msg["content"]
                        })
                
                # Make API call
                result = openai_service.chat_completion_with_history(
                    conversation,
                    model=selected_model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                if result['success']:
                    st.write(result['response'])
                    
                    # Add assistant response to history
                    assistant_message = {
                        "role": "assistant",
                        "content": result['response']
                    }
                    st.session_state.chat_history.append(assistant_message)
                    
                    # Show usage info
                    if 'usage' in result and result['usage']:
                        with st.expander("📊 Usage Information"):
                            usage = result['usage']
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Prompt Tokens", usage.get('prompt_tokens', 0))
                            with col2:
                                st.metric("Completion Tokens", usage.get('completion_tokens', 0))
                            with col3:
                                st.metric("Total Tokens", usage.get('total_tokens', 0))
                else:
                    st.error(f"Error: {result['error']}")


def _process_uploaded_file(file) -> Optional[str]:
    """
    Process uploaded file and extract text content.
    
    Args:
        file: Uploaded file object
        
    Returns:
        Extracted text content or None if processing failed
    """
    try:
        # Read file content
        file_content = file.read()
        
        # Handle different file types
        if file.type.startswith('text/'):
            # Text files
            return file_content.decode('utf-8')
        
        elif file.type == 'application/json':
            # JSON files
            import json
            try:
                json_data = json.loads(file_content.decode('utf-8'))
                return json.dumps(json_data, indent=2)
            except json.JSONDecodeError:
                return file_content.decode('utf-8')
        
        elif file.type == 'text/csv':
            # CSV files
            import pandas as pd
            try:
                df = pd.read_csv(io.BytesIO(file_content))
                return df.to_string()
            except Exception:
                return file_content.decode('utf-8')
        
        elif file.type.startswith('image/'):
            # Image files - encode as base64 for now
            # In a real implementation, you might want to use vision models
            base64_image = base64.b64encode(file_content).decode('utf-8')
            return f"[Image: {file.name} - Base64 encoded, {len(base64_image)} characters]"
        
        else:
            # For other file types, try to decode as text
            try:
                return file_content.decode('utf-8')
            except UnicodeDecodeError:
                return f"[Binary file: {file.name} - {file.size} bytes]"
    
    except Exception as e:
        logging.error(f"Error processing file {file.name}: {e}")
        return f"[Error processing file: {file.name}]"


def render_chat_help() -> None:
    """
    Render help section for the chat interface.
    """
    st.subheader("❓ How to Use")
    
    with st.expander("Getting Started"):
        st.markdown("""
        **1. API Key Setup:**
        - Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
        - Enter it in the text input field above
        
        **2. Chat Features:**
        - Type your message in the chat input
        - Upload files to get help with their content
        - Use the sidebar to adjust model settings
        
        **3. File Upload:**
        - Supported formats: TXT, PDF, DOCX, PNG, JPG, CSV, JSON
        - Files are processed and included in your conversation
        - Images are base64 encoded for processing
        """)
    
    with st.expander("Tips & Best Practices"):
        st.markdown("""
        **💡 Tips:**
        - Be specific in your questions
        - Upload relevant files for better context
        - Use system messages to set AI behavior
        - Adjust temperature for creativity vs. focus
        
        **🔧 Settings:**
        - **Temperature**: Lower = more focused, Higher = more creative
        - **Max Tokens**: Controls response length
        - **System Message**: Sets AI personality and behavior
        
        **📁 File Processing:**
        - Text files are read directly
        - CSV files are converted to readable format
        - Images are base64 encoded
        - JSON files are formatted for readability
        """)
    
    with st.expander("Troubleshooting"):
        st.markdown("""
        **Common Issues:**
        - **API Key Error**: Check your key is valid and has credits
        - **Rate Limit**: Wait a moment and try again
        - **File Upload Issues**: Check file format and size
        - **Connection Error**: Check your internet connection
        
        **Getting Help:**
        - Check OpenAI status page for API issues
        - Verify your API key has sufficient credits
        - Try different models if one fails
        """)
