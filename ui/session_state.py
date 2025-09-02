import streamlit as st
from ai_services import get_embedding
from config import ROLE_DESCRIPTIONS, OLLAMA_EMBED_MODEL


def initialize_session_state():
    """Initialize all session state variables."""
    
    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Current manifest data
    if 'current_manifest' not in st.session_state:
        st.session_state.current_manifest = {
            "characters": "", 
            "setting": "", 
            "story": "", 
            "style": ""
        }
    
    # Current prompt
    if 'current_prompt' not in st.session_state:
        st.session_state.current_prompt = ""
    
    # Advanced options form
    if 'advanced_options_form' not in st.session_state:
        st.session_state.advanced_options_form = {
            "lighting": "", 
            "color_palette": "", 
            "camera_angle": "", 
            "composition": "",
            "time_of_day": "", 
            "weather_effects": "", 
            "textures": "", 
            "props": "",
            "flora_fauna": "", 
            "architecture_details": "", 
            "environment_hazards": "",
            "mood_atmosphere": "", 
            "character_emotions": "", 
            "artist_references": "",
            "genre_subgenre": "", 
            "medium": "", 
            "aspect_ratio": "", 
            "resolution_detail": ""
        }
    
    # UI state flags
    if 'show_form_only' not in st.session_state:
        st.session_state.show_form_only = True
    
    if 'generating_initial_prompt' not in st.session_state:
        st.session_state.generating_initial_prompt = False
    
    if 'processing_refinement' not in st.session_state:
        st.session_state.processing_refinement = False
    
    if 'image_generation_status' not in st.session_state:
        st.session_state.image_generation_status = None
    
    if 'is_editing_prompt' not in st.session_state:
        st.session_state.is_editing_prompt = False
    
    # Pre-calculate role embeddings once at startup
    if 'role_embeddings' not in st.session_state:
        st.session_state.role_embeddings = {}
        with st.spinner(f"Loading embedding model '{OLLAMA_EMBED_MODEL}' and preparing role definitions..."):
            for role, description in ROLE_DESCRIPTIONS.items():
                st.session_state.role_embeddings[role] = get_embedding(description)
        
        if any(len(e) == 0 for e in st.session_state.role_embeddings.values()):
            st.error("Failed to load embeddings for one or more roles. Please check Ollama server and model.")
            st.stop()


def reset_all_session_state():
    """Reset all session state variables."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Reinitialize with defaults
    st.session_state.show_form_only = True
    st.session_state.processing_refinement = False
    st.session_state.generating_initial_prompt = False
    st.session_state.image_generation_status = None
    st.session_state.is_editing_prompt = False


def is_any_ai_processing():
    """Check if any AI processing is currently active."""
    return (st.session_state.generating_initial_prompt or 
            st.session_state.processing_refinement or 
            (st.session_state.image_generation_status == 'generating') or 
            st.session_state.is_editing_prompt)