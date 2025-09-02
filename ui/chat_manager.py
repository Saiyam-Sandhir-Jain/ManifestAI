import streamlit as st
from datetime import datetime


def add_message(role, content, timestamp=None, is_image=False):
    """Add a message to the chat history."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    st.session_state.chat_history.append({
        "role": role,
        "content": content,
        "timestamp": timestamp,
        "is_image": is_image
    })


def display_chat_message(message):
    """Display a single chat message."""
    if message["role"] == "user":
        formatted_content = message["content"].replace('\n', '<br>')
        st.markdown(f"""
        <div class="chat-message">
            <div class="user-message">
                <div class="message-header user-header">You • {message["timestamp"]}</div>
                <div class="user-bubble">{formatted_content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:  # Assistant messages
        content = message["content"]
        if message.get("is_image"):
            st.markdown(f"""
            <div class="chat-message">
                <div class="assistant-message">
                    <div class="message-header assistant-header">🎨 Manifest AI • {message["timestamp"]}</div>
                    <div class="assistant-bubble" style="padding: 0; overflow: hidden; border-radius: 18px 18px 18px 4px;">
                        <img src="{content}" style="max-width: 100%; height: auto; display: block; border-radius: 16px 16px 16px 2px;" alt="AI Generated Image" />
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if "```" in content:
                parts = content.split("```")
                formatted_content = parts[0]
                if len(parts) >= 3:
                    code_block_html = f'<div class="prompt-display">{parts[1].strip()}</div>'
                    formatted_content += code_block_html + parts[2]
                else:
                    formatted_content = content
            else:
                formatted_content = content.replace('\n', '<br>')

            st.markdown(f"""
            <div class="chat-message">
                <div class="assistant-message">
                    <div class="message-header assistant-header">🎨 Manifest AI • {message["timestamp"]}</div>
                    <div class="assistant-bubble">{formatted_content}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def display_chat_history():
    """Display the complete chat history."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    for message in st.session_state.chat_history:
        display_chat_message(message)