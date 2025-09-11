import streamlit as st
from datetime import datetime
import time
from dotenv import load_dotenv

load_dotenv() 

# Import our modular components
from ui.session_state import initialize_session_state, is_any_ai_processing
from ui.ui_components import (
    get_css_styles, 
    render_initial_form, 
    validate_form_inputs, 
    process_form_submission,
    render_edit_prompt_section
)
from ui.sidebar_components import render_sidebar
from ui.chat_manager import display_chat_history, add_message
from ai.prompt_intelligence import handle_assistant_response_streaming
from ai.ai_services import refine_prompt, generate_image

# Configure page
st.set_page_config(
    layout="wide",
    page_title="Manifest AI",
    page_icon="🎨"
)

# Apply CSS styles
st.markdown(get_css_styles(), unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# Header
st.markdown('<h1 class="main-title">🎨 Manifest AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Craft your visions into stunning images with AI.</p>', unsafe_allow_html=True)

# Main application logic
def main():
    """Main application logic."""
    
    # Conditional Rendering: Initial Form vs. Chat UI
    if st.session_state.show_form_only:
        render_form_view()
    else:
        render_chat_view()
    
    # Render sidebar
    render_sidebar()
    
    # Auto-scroll JavaScript
    render_auto_scroll_script()


def render_form_view():
    """Render the initial form view."""
    submit_button, characters_input, setting_input, story_input, style_input = render_initial_form()
    
    if submit_button:
        missing_fields = validate_form_inputs(characters_input, setting_input, story_input, style_input)
        
        if missing_fields:
            st.error(f"Please fill in all **Required Basic Details**: {', '.join([f'**{f}**' for f in missing_fields])}")
        else:
            process_form_submission(characters_input, setting_input, story_input, style_input)
            st.rerun()


def render_chat_view():
    """Render the chat interface view."""
    # Scroll to top when chat UI first appears
    if st.session_state.get('scroll_to_top_on_chat_init', True):
        st.markdown("<script>window.scrollTo(0, 0);</script>", unsafe_allow_html=True)
        st.session_state.scroll_to_top_on_chat_init = False

    # Chat history display container
    st.markdown('<div class="chat-history-container" id="chat-history-scroll-container">', unsafe_allow_html=True)
    display_chat_history()
    st.markdown('</div>', unsafe_allow_html=True)

    # Handle different processing states
    handle_initial_prompt_generation()
    handle_image_generation()
    handle_refinement_processing()
    
    # Edit prompt section
    render_edit_prompt_section()
    
    # Chat input
    handle_chat_input()


def handle_initial_prompt_generation():
    """Handle initial prompt generation process."""
    if st.session_state.generating_initial_prompt:
        with st.spinner("✨ Generating your initial manifestation..."):
            full_manifest = {**st.session_state.current_manifest, **st.session_state.advanced_options_form}
            generated_prompt = refine_prompt(full_manifest, "expert prompt engineer")
        
        st.session_state.generating_initial_prompt = False
        
        handle_assistant_response_streaming(
            user_query_for_llm=None,
            current_prompt=st.session_state.current_prompt,
            current_manifest_components=st.session_state.current_manifest,
            initial_refined_output=generated_prompt,
            is_initial_generation=True
        )
        st.rerun()


def handle_image_generation():
    """Handle image generation process."""
    if st.session_state.image_generation_status == 'generating':
        with st.chat_message("assistant"):
            with st.spinner("⏳ Generating your image..."):
                image_url = generate_image(st.session_state.current_prompt)
            
            if image_url:
                add_message("assistant", image_url, is_image=True)
                st.markdown(f"""
                <div class="assistant-bubble" style="padding: 0; overflow: hidden; border-radius: 18px 18px 18px 4px;">
                    <img src="{image_url}" style="max-width: 100%; height: auto; display: block; border-radius: 16px 16px 16px 2px;" alt="AI Generated Image" />
                </div>
                """, unsafe_allow_html=True)
                st.session_state.image_generation_status = 'finished_success'
            else:
                error_message = "❌ Image generation failed. Please try again."
                add_message("assistant", error_message, is_image=False)
                st.markdown(f'<div class="assistant-bubble">{error_message}</div>', unsafe_allow_html=True)
                st.session_state.image_generation_status = 'finished_failure'
        
        st.rerun()

    # Reset image generation status after UI has updated
    if st.session_state.image_generation_status in ['finished_success', 'finished_failure']:
        st.session_state.image_generation_status = None


def handle_refinement_processing():
    """Handle refinement processing."""
    if st.session_state.processing_refinement and not st.session_state.generating_initial_prompt:
        latest_user_message_content = st.session_state.chat_history[-1]["content"]
        st.session_state.processing_refinement = False

        with st.spinner("🧠 Manifest AI is thinking..."):
            handle_assistant_response_streaming(
                latest_user_message_content,
                st.session_state.current_prompt,
                st.session_state.current_manifest,
                is_initial_generation=False
            )
        st.rerun()


def handle_chat_input():
    """Handle chat input processing."""
    user_query = st.chat_input(
        "Refine your manifestation or ask for the next scene...",
        key="chat_input_refine", 
        disabled=is_any_ai_processing()
    )

    if user_query:
        add_message("user", user_query)
        st.session_state.processing_refinement = True
        st.rerun()


def render_auto_scroll_script():
    """Render the auto-scroll JavaScript."""
    st.markdown("""
    <script>
        function scrollToBottom() {
            const container = document.getElementById('chat-history-scroll-container');
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        }

        const chatHistoryObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.addedNodes.length > 0) {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === 1 && node.classList.contains('chat-message')) {
                            node.style.opacity = '1';
                            node.style.transform = 'translateY(0) scale(1)';
                        }
                    });
                    setTimeout(scrollToBottom, 0); 
                }
            });
        });

        const container = document.getElementById('chat-history-scroll-container');
        if (container) {
            chatHistoryObserver.observe(container, {
                childList: true,
                subtree: true
            });
            setTimeout(scrollToBottom, 0);
        }
    </script>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()