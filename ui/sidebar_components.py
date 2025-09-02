import streamlit as st
from datetime import datetime
from chat_manager import add_message
from session_state import is_any_ai_processing
import random


def get_css_styles():
    """Return the CSS styles for the application."""
    return """
    <style>
        /* Hide Streamlit branding */
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
         
        /* Main container styling */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1200px;
            display: flex;
            flex-direction: column;
            height: calc(100vh - 40px);
        }
         
        /* Responsive breakpoints */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
        }
         
        /* Chat history container - makes it scrollable */
        .chat-history-container {
            flex-grow: 1;
            overflow-y: auto;
            padding: 0 1rem;
            margin-bottom: 1rem;
        }

        /* Fixed input container at the bottom */
        .stChatInputContainer {
            position: sticky;
            bottom: 0;
            background-color: white;
            z-index: 1000;
            padding: 1rem 0;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        }

        /* Message styling */
        .chat-message {
            margin: 1rem 0;
            display: flex;
            flex-direction: column;
            width: 100%;
        }
         
        .user-message {
            align-self: flex-end;
            max-width: 85%;
        }
         
        .user-bubble {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            border-radius: 18px 18px 4px 18px;
            padding: 12px 18px;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);
            font-size: 15px;
            line-height: 1.5;
            word-wrap: break-word;
            margin-left: auto;
        }
         
        .assistant-bubble {
            background: #f1f5f9;
            color: #1e293b;
            border-radius: 18px 18px 18px 4px;
            padding: 16px 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border: 1px solid #e2e8f0;
            font-size: 15px;
            line-height: 1.6;
            word-wrap: break-word;
        }
         
        .message-header {
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 8px;
            opacity: 0.8;
        }
         
        .user-header {
            color: rgba(255, 255, 255, 0.9);
            text-align: right;
        }
         
        .assistant-header {
            color: #64748b;
            text-align: left;
        }
         
        .prompt-display {
            background: #000000;
            color: #ffffff;
            border-radius: 8px;
            padding: 16px;
            font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
            margin: 12px 0;
            border: 1px solid #374151;
            max-height: none;
            overflow: visible;
        }
         
        .main-title {
            text-align: center;
            color: #1e293b;
            margin-bottom: 1rem;
            font-weight: 700;
            font-size: clamp(1.8rem, 4vw, 2.5rem);
        }
         
        .main-subtitle {
            text-align: center;
            color: #64748b;
            margin-bottom: 2rem;
            font-size: clamp(0.9rem, 2vw, 1.1rem);
        }
         
        .welcome-message {
            background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
            border: 2px solid #0ea5e9;
            border-radius: 16px;
            padding: 20px;
            margin: 1rem 0;
            color: #0c4a6e;
            font-size: 15px;
            line-height: 1.7;
        }
         
        .welcome-message strong {
            color: #0369a1;
        }

        .stChatInput {
            width: 100%;
            margin: 0 auto;
            max-width: 800px;
        }

        .element-container {
            margin-bottom: 0 !important;
        }

        .css-1rs6itu.e1vispgu1 {
            margin-bottom: 0 !important;
        }

        .stSidebar .stButton>button {
            background: linear-gradient(135deg, #4f46e5, #4338ca) !important;
            box-shadow: 0 2px 8px rgba(79, 70, 229, 0.2) !important;
        }
        .stSidebar .stButton>button:hover {
            background: linear-gradient(135deg, #4338ca, #3730a3) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
        }

        .form-section {
            background: #f8fafc;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid #e2e8f0;
        }
    </style>
    """


def render_initial_form():
    """Render the initial manifestation form."""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 📝 Define Your Initial Image Concept")
    st.info("Fill in the basic details, and add advanced options for greater control.")

    with st.form("initial_manifestation_form", clear_on_submit=False):
        col1, col2 = st.columns(2, gap="medium")

        with col1:
            characters_input = st.text_input(
                "Characters *",
                value=st.session_state.current_manifest.get("characters", ""),
                placeholder="e.g., heroic knight, wise wizard",
                help="Describe the main characters or subjects in your image",
                key="form_characters_input"
            )
            setting_input = st.text_input(
                "Setting *",
                value=st.session_state.current_manifest.get("setting", ""),
                placeholder="e.g., mystical forest, futuristic city",
                help="Describe the environment or location",
                key="form_setting_input"
            )

        with col2:
            story_input = st.text_area(
                "Story/Action *",
                value=st.session_state.current_manifest.get("story", ""),
                placeholder="e.g., battling a dragon, casting a spell",
                height=100,
                help="Describe what's happening in the scene",
                key="form_story_input"
            )
            style_input = st.text_input(
                "Art Style *",
                value=st.session_state.current_manifest.get("style", ""),
                placeholder="e.g., digital painting, photorealistic",
                help="Describe the artistic style and influences",
                key="form_style_input"
            )

        # Advanced options
        with st.expander("🎛️ Advanced Options (Optional)", expanded=False):
            st.markdown("Add more specific details to enhance your manifestation.")
            cols_adv = st.columns(2)
            with cols_adv[0]:
                st.session_state.advanced_options_form["lighting"] = st.text_input(
                    "**Lighting**",
                    value=st.session_state.advanced_options_form.get("lighting", ""),
                    placeholder="e.g., cinematic, dramatic, soft, neon",
                    key="form_advanced_lighting",
                    disabled=is_any_ai_processing()
                )
                st.session_state.advanced_options_form["camera_angle"] = st.text_input(
                    "**Camera Angle**",
                    value=st.session_state.advanced_options_form.get("camera_angle", ""),
                    placeholder="e.g., wide shot, close-up, bird's eye view",
                    key="form_advanced_camera_angle",
                    disabled=is_any_ai_processing()
                )
            with cols_adv[1]:
                st.session_state.advanced_options_form["color_palette"] = st.text_input(
                    "**Color Palette**",
                    value=st.session_state.advanced_options_form.get("color_palette", ""),
                    placeholder="e.g., warm, cool, monochromatic, vibrant",
                    key="form_advanced_color_palette",
                    disabled=is_any_ai_processing()
                )
                st.session_state.advanced_options_form["composition"] = st.text_input(
                    "**Composition**",
                    value=st.session_state.advanced_options_form.get("composition", ""),
                    placeholder="e.g., rule of thirds, leading lines, symmetrical",
                    key="form_advanced_composition",
                    disabled=is_any_ai_processing()
                )

        submit_button = st.form_submit_button(
            "🎯 Generate Initial Manifestation",
            type="primary", 
            use_container_width=True,
            disabled=is_any_ai_processing()
        )

        return submit_button, characters_input, setting_input, story_input, style_input

    st.markdown('</div>', unsafe_allow_html=True)


def validate_form_inputs(characters_input, setting_input, story_input, style_input):
    """Validate form inputs and return missing fields."""
    missing_basic_fields = []
    
    if not characters_input.strip():
        missing_basic_fields.append("Characters")
    if not setting_input.strip():
        missing_basic_fields.append("Setting")
    if not story_input.strip():
        missing_basic_fields.append("Story/Action")
    if not style_input.strip():
        missing_basic_fields.append("Art Style")
    
    return missing_basic_fields


def process_form_submission(characters_input, setting_input, story_input, style_input):
    """Process the form submission and update session state."""
    # Update manifest from form inputs
    st.session_state.current_manifest.update({
        "characters": characters_input,
        "setting": setting_input,
        "story": story_input,
        "style": style_input
    })
    
    # Build advanced_from_form by including only non-empty advanced options
    advanced_from_form = {}
    for key, value in st.session_state.advanced_options_form.items():
        if value.strip():
            advanced_from_form[key] = value

    st.session_state.advanced_options_form = advanced_from_form

    # Add user's form submission summary to chat history
    form_summary = f"Characters: {characters_input}\nSetting: {setting_input}\nStory: {story_input}\nStyle: {style_input}"
    if advanced_from_form:
        adv_items = [f"{k.replace('_', ' ').title()}: {v}" for k, v in advanced_from_form.items()]
        form_summary += f"\nAdvanced Options: {', '.join(adv_items)}"
    add_message("user", "Initial manifestation form submitted:\n\n" + form_summary)

    # Set flags to transition to chat UI and start generation
    st.session_state.show_form_only = False
    st.session_state.generating_initial_prompt = True


def render_edit_prompt_section():
    """Render the edit prompt section."""
    if st.session_state.current_prompt and st.session_state.chat_history:
        if "```" in st.session_state.chat_history[-1].get("content", ""):
            if not st.session_state.is_editing_prompt:
                st.markdown('<div class="button-container">', unsafe_allow_html=True)
                if st.button("✏️ Edit Manifest Manually", key="edit_prompt_button", disabled=is_any_ai_processing()):
                    st.session_state.is_editing_prompt = True
                    st.rerun()
                if st.button(
                    "🖼️ Generate Image", 
                    key="generate_image_button_top", 
                    type="secondary", 
                    help="Generate an image from the current manifestation",
                    disabled=is_any_ai_processing() or not st.session_state.current_prompt
                ):
                    st.session_state.image_generation_status = 'generating'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                render_edit_mode()


def render_edit_mode():
    """Render the edit mode interface."""
    edited_prompt_container = st.container()
    with edited_prompt_container:
        edited_prompt_value = st.text_area(
            "**Edit Manifestation**",
            value=st.session_state.current_prompt,
            height=250,
            key="editable_prompt_text_area"
        )
    
    edit_buttons_col1, edit_buttons_col2 = st.columns([0.15, 0.85])
    with edit_buttons_col1:
        if st.button("✅ Save", key="save_edited_prompt", type="primary"):
            st.session_state.current_prompt = edited_prompt_value
            st.session_state.is_editing_prompt = False
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"✅ Manifestation updated manually:\n\n```\n{st.session_state.current_prompt}\n```",
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    with edit_buttons_col2:
        if st.button("❌ Cancel", key="cancel_edit_prompt"):
            st.session_state.is_editing_prompt = False
            st.rerun()


def get_random_manifestation_data():
    """Generate random manifestation data."""
    character_descriptors = [
        "grizzled veteran", "young prodigy", "ancient sage", "fearless leader",
        "mysterious stranger", "reclusive inventor", "charming rogue",
        "stoic warrior", "nimble scout", "wise elder", "brash adventurer",
        "melancholy artist", "eccentric scientist", "cunning politician",
        "honorable guard", "resourceful survivor", "shadowy assassin",
        "heroic champion", "kind healer", "rebellious youth"
    ]
    
    character_roles = [
        "knight", "wizard", "hacker", "detective", "pilot", "mercenary",
        "engineer", "bard", "monk", "archaeologist", "gladiator", "shaman",
        "diplomat", "rebel", "enforcer", "alchemist", "bounty hunter",
        "scribe", "spy", "robot"
    ]
    
    relationships = [
        "allied with", "rival to", "mentoring", "betrayed by", "seeking",
        "protecting", "conspiring with", "estranged from", "bound to",
        "on a quest with", "hunting", "rescued by", "guided by",
        "at odds with", "loyal to", "befriended by"
    ]

    num_characters = random.randint(1, 3)
    generated_characters = []
    for i in range(num_characters):
        descriptor = random.choice(character_descriptors)
        role = random.choice(character_roles)
        generated_characters.append(f"{descriptor} {role}")

    final_characters_string = ""
    if len(generated_characters) == 1:
        final_characters_string = generated_characters[0]
    elif len(generated_characters) == 2:
        rel = random.choice(relationships)
        final_characters_string = f"{generated_characters[0]} {rel} {generated_characters[1]}"
    else:
        rel1 = random.choice(relationships)
        rel2 = random.choice(relationships)
        final_characters_string = (
            f"{generated_characters[0]} {rel1} {generated_characters[1]}, "
            f"and {generated_characters[2]}."
        )

    settings = [
        "glowing mushroom forest under twin moons",
        "ruined alien city overgrown with phosphorescent flora",
        "nebula-filled cosmos with swirling galaxies and ancient cosmic entities",
        "steampunk metropolis shrouded in perpetual smog and clockwork towers",
        "post-apocalyptic desert with colossal sand worms and scavengers",
        "underwater bioluminescent cavern filled with ancient secrets and mythical creatures",
        "floating sky-city powered by arcane crystals and airship docks",
        "dystopian cityscape bathed in neon rain and towering corporate monoliths",
        "a forgotten temple deep within an enchanted jungle with hidden traps",
        "a bustling futuristic spaceport at sunset with diverse alien species"
    ]

    stories = [
        "defending a crystal artifact from shadowy invaders",
        "discovering a forgotten technology that could change the world forever",
        "navigating a treacherous asteroid field to deliver vital cargo",
        "solving an ancient riddle that guards a hidden realm of power",
        "engaging in aerial combat against a fleet of enemy airships",
        "embarking on a quest to restore a broken prophecy and bring balance",
        "evading robotic patrols in a high-security facility",
        "conducting a ritual under a blood moon to summon a forgotten deity",
        "searching for a lost civilization's treasure in a treacherous labyrinth",
        "performing a daring rescue operation in zero gravity amidst debris"
    ]

    styles = [
        "surreal digital art with vibrant, clashing colors and dreamlike compositions",
        "vaporwave illustration with dreamlike pastels, retro aesthetics, and glowing grids",
        "epic fantasy oil painting with intricate details, high realism, and dramatic lighting",
        "retro sci-fi poster art, reminiscent of 1970s pulp covers, bold lines, muted colors",
        "gritty graphic novel style with heavy line work, dynamic shadows, and muted palette",
        "cel-shaded anime style with exaggerated expressions, vibrant colors, and dynamic poses",
        "photorealistic cinematic render with dramatic lighting, deep shadows, and rich textures",
        "impressionistic oil painting with soft brushstrokes, vibrant colors, and atmospheric blur",
        "cyberpunk noir, high contrast with deep shadows, neon accents, and rainy streets",
        "watercolor illustration, ethereal and dreamlike, with soft edges and luminous washes"
    ]

    return {
        "characters": final_characters_string,
        "setting": random.choice(settings),
        "story": random.choice(stories),
        "style": random.choice(styles)
    }


def get_example_data(example_type):
    """Get example data for different manifestation types."""
    examples = {
        "fantasy": {
            "characters": "wise elven mage with glowing staff",
            "setting": "ancient mystical forest with floating islands",
            "story": "casting a powerful protection spell",
            "style": "detailed fantasy art, digital painting"
        },
        "scifi": {
            "characters": "cyberpunk hacker with neural implants",
            "setting": "neon-lit futuristic city with holographic displays",
            "story": "infiltrating a massive corporate database",
            "style": "cinematic cyberpunk art, high contrast lighting"
        }
    }
    return examples.get(example_type, examples["fantasy"])
