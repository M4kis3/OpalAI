import streamlit as st
import requests
import uuid
import json

# Constants
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/invoke_n8n_agent"  # Replace with your n8n webhook URL
BEARER_TOKEN = "cake"  # Replace with your bearer token
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}

def initialize_session():
    """Initialize session state variables if they don't exist"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    """Display the chat history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def send_message_to_n8n(message):
    """Send message to n8n webhook and return response"""
    payload = {
        "sessionId": st.session_state.session_id,
        "chatInput": message
    }
    
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            headers=HEADERS,
            json=payload
        )
        response.raise_for_status()
        return response.json()["output"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with n8n: {str(e)}")
        return None

def main():
    st.title("Chat with AI")
    
    # Initialize session
    initialize_session()
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message_to_n8n(prompt)
                if response:
                    st.write(response)
                    # Add assistant response to chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )

if __name__ == "__main__":
    main()