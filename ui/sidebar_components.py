import streamlit as st
from .ui_components import get_example_data, get_random_manifestation_data
from .session_state import is_any_ai_processing, reset_all_session_state


def render_sidebar():
    """Render the sidebar with examples and actions."""
    with st.sidebar:
        st.markdown("### 💡 Examples")
        
        # Fantasy Example Button
        if st.button("🧙‍♂️ Fantasy Example", use_container_width=True, disabled=is_any_ai_processing()):
            set_example_data("fantasy")

        # Sci-Fi Example Button
        if st.button("🚀 Sci-Fi Example", use_container_width=True, disabled=is_any_ai_processing()):
            set_example_data("scifi")
        
        # Random Manifestation Button
        if st.button("🎲 Random Manifestation", use_container_width=True, disabled=is_any_ai_processing()):
            set_random_data()
        
        st.divider()
        
        # Start Over Button
        if st.button("🔥 Start Over", use_container_width=True, disabled=is_any_ai_processing()):
            reset_all_session_state()
            st.rerun()


def set_example_data(example_type):
    """Set example data and reset to form view."""
    example_data = get_example_data(example_type)
    st.session_state.current_manifest = example_data
    
    # Reset advanced options
    st.session_state.advanced_options_form = {
        "lighting": "", "color_palette": "", "camera_angle": "", "composition": ""
    }
    
    reset_to_form_view()


def set_random_data():
    """Set random manifestation data and reset to form view."""
    st.session_state.current_manifest = get_random_manifestation_data()
    
    # Reset advanced options
    st.session_state.advanced_options_form = {
        "lighting": "", "color_palette": "", "camera_angle": "", "composition": ""
    }
    
    reset_to_form_view()


def reset_to_form_view():
    """Reset session state to show the form with pre-filled data."""
    st.session_state.show_form_only = True
    st.session_state.chat_history = []
    st.session_state.processing_refinement = False
    st.session_state.generating_initial_prompt = False
    st.session_state.image_generation_status = None
    st.session_state.is_editing_prompt = False
    st.rerun()