import streamlit as st
import time
from datetime import datetime
from .ai_services import get_embedding, cosine_similarity, refine_prompt
from ui.chat_manager import add_message
from .config import SIMILARITY_THRESHOLD


def determine_and_refine_prompt(user_query, current_prompt, current_manifest_components):
    """Intelligently determine role and refine prompt using embeddings."""
    user_query_lower = user_query.lower()

    # If no current prompt exists, always prompt for initial generation
    if not current_prompt:
        return None, "⚠️ Please generate an initial manifestation first using the form.", None

    # Generate embedding for the user's query
    user_query_embedding = get_embedding(user_query)
    if len(user_query_embedding) == 0:
        return None, "❌ Failed to generate embedding for your query. Please try again or check Ollama server.", None

    best_match_role = "prompt editor"  # Default if no strong semantic match
    max_similarity = -1

    # Temporarily prioritize acknowledgement if it's a short, positive feedback
    is_short_positive_feedback = False
    ack_keywords = ["good", "nice", "perfect", "great", "excellent", "awesome", "love it", "superb", "fantastic", "thanks", "okay", "got it"]
    if len(user_query_lower.split()) <= 3 and any(keyword in user_query_lower for keyword in ack_keywords):
        best_match_role = "acknowledgement_responder"
        max_similarity = 1.0
        is_short_positive_feedback = True

    if not is_short_positive_feedback:
        # Compare user query embedding with pre-calculated role embeddings
        for role, role_embedding in st.session_state.role_embeddings.items():
            if role == "acknowledgement_responder":
                continue
            similarity = cosine_similarity(user_query_embedding, role_embedding)
            if similarity > max_similarity:
                max_similarity = similarity
                best_match_role = role

    final_role_for_ollama_call = best_match_role
    status_prefix = ""

    # Handle special cases or apply a threshold
    if max_similarity < SIMILARITY_THRESHOLD and not is_short_positive_feedback:
        final_role_for_ollama_call = "prompt editor"
        status_prefix = "✨ Using general editing for your request:"
    elif final_role_for_ollama_call == "style_blender":
        # First, call style_blender role to get the blended style description
        blended_style_manifest = {"user_changes": user_query}
        blended_style_description = refine_prompt(blended_style_manifest, "style_blender")
        
        if blended_style_description and not blended_style_description.startswith("Error:"):
            # Now, integrate the blended style description into the current prompt using the prompt editor
            manifest_for_refinement_to_editor = {
                "original_prompt": current_prompt,
                "user_changes": f"Integrate the blended style '{blended_style_description}' into the prompt's style section."
            }
            refined_output_final = refine_prompt(manifest_for_refinement_to_editor, "prompt editor")
            return refined_output_final, f"🎨 Blended styles and applied to prompt:", "prompt editor"
        else:
            final_role_for_ollama_call = "prompt editor"
            status_prefix = f"❌ Blending styles failed with error: {blended_style_description}. Defaulting to general editor:"

    # Set default status prefix if not already set by special handling
    if not status_prefix:
        status_prefixes = {
            "alternative_story_generator": "💡 Alternative Generated!",
            "next_scene_generator": "⏩ Next Scene Generated!",
            "rephrase_manifestation_generator": "✏️ Manifestation Rephrased!",
            "acknowledgement_responder": "👍 Understood!",
            "prompt editor": "✅ Applied your changes and refined the manifestation:"
        }
        status_prefix = status_prefixes.get(final_role_for_ollama_call, "✅ Applied your changes and refined the manifestation:")

    # Determine manifest_for_refinement based on final_role_for_ollama_call
    manifest_mappings = {
        "alternative_story_generator": {
            "current_characters": current_manifest_components.get("characters", ""),
            "current_setting": current_manifest_components.get("setting", ""),
            "current_style": current_manifest_components.get("style", ""),
            "user_specific_request": user_query
        },
        "next_scene_generator": {
            "previous_prompt_text": current_prompt,
            "user_request": user_query
        },
        "rephrase_manifestation_generator": {
            "prompt_to_rephrase": current_prompt
        },
        "acknowledgement_responder": {
            "user_feedback": user_query
        },
        "prompt editor": {
            "original_prompt": current_prompt,
            "user_changes": user_query
        }
    }

    manifest_for_refinement = manifest_mappings.get(final_role_for_ollama_call, {
        "original_prompt": current_prompt,
        "user_changes": user_query
    })

    if final_role_for_ollama_call not in manifest_mappings:
        final_role_for_ollama_call = "prompt editor"

    refined_output = refine_prompt(manifest_for_refinement, final_role_for_ollama_call)
    return refined_output, status_prefix, final_role_for_ollama_call


def handle_assistant_response_streaming(user_query_for_llm, current_prompt, current_manifest_components, initial_refined_output=None, is_initial_generation=False):
    """Handle the assistant's response streaming with loading indicator."""
    if is_initial_generation:
        refined_output = initial_refined_output
        status_message = "🎯 Initial manifestation generated!"
        executed_role = "expert prompt engineer"
    else:
        refined_output, status_message, executed_role = determine_and_refine_prompt(
            user_query_for_llm,
            current_prompt,
            current_manifest_components
        )
    
    # Prepare the final response content
    if refined_output and not refined_output.startswith("Error:"):
        # Update current_prompt only if it's an actual prompt
        if executed_role not in ["acknowledgement_responder", None]:
            st.session_state.current_prompt = refined_output

        # Determine the full response content
        if executed_role == "acknowledgement_responder":
            response_to_chat = f"{status_message} {refined_output}"
        elif refined_output.strip() == "":
            response_to_chat = f"{status_message} No specific changes made or output generated."
        elif status_message.startswith("⚠️"):
            response_to_chat = f"{status_message} {refined_output}"
        else:
            response_to_chat = f"{status_message}\n\n```\n{refined_output}\n```"
        
        # Display the message in an assistant chat bubble and stream content
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_streamed_response = ""
            words = response_to_chat.split()
            for chunk in words:
                full_streamed_response += chunk + " "
                time.sleep(0.01)
                message_placeholder.markdown(full_streamed_response)
        
        add_message("assistant", full_streamed_response)
    else:
        with st.chat_message("assistant"):
            error_message = f"❌ Operation Failed! Sorry, I couldn't process your request: {status_message}. Please try again."
            st.markdown(error_message)
            add_message("assistant", error_message)

    st.session_state.processing_refinement = False