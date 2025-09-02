import ollama
import json
import requests
import numpy as np
import streamlit as st
from config import OLLAMA_BASE_URL, OLLAMA_EMBED_MODEL


def get_embedding(text):
    """Get embeddings from Ollama for the given text."""
    try:
        client = ollama.Client(host=OLLAMA_BASE_URL)
        response = client.embeddings(model=OLLAMA_EMBED_MODEL, prompt=text)
        return np.array(response['embedding'])
    except Exception as e:
        st.error(f"Error getting embedding from Ollama (model: {OLLAMA_EMBED_MODEL}): {e}. Make sure '{OLLAMA_EMBED_MODEL}' is installed and Ollama server is running.")
        return np.array([])


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    if len(vec1) == 0 or len(vec2) == 0:
        return 0
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0
    return dot_product / (norm_vec1 * norm_vec2)


def refine_prompt(user_manifest, system_role="expert prompt engineer"):
    """Refine prompt using Ollama with different system roles."""
    client = ollama.Client(host=OLLAMA_BASE_URL)

    system_prompts = {
        "expert prompt engineer": (
            "You are an expert prompt engineer for an AI image generator. "
            "Your task is to take a structured user manifestation (in JSON format) "
            "and combine its components into a single, cohesive, and highly detailed "
            "text prompt for an AI image model. The user will provide a JSON object "
            "containing fields like 'characters', 'setting', 'story', 'style', "
            "and potentially advanced details. "
            "Your output must be only the refined prompt, without any extra commentary. "
            "Ensure the final prompt flows naturally and integrates all elements."
        ),
        "prompt editor": (
            "You are a prompt editor for an AI image generator. "
            "You will receive an existing prompt in the 'original_prompt' key and user-requested changes in 'user_changes'. "
            "Your task is to integrate these changes smoothly into the existing prompt, producing a new, refined prompt. "
            "**Your capabilities include:**\n"
            "* **General edits:** Adding, removing, or modifying elements.\n"
            "* **Stylistic changes:** Rephrasing to make it shorter, longer, simpler, or more descriptive.\n"
            "* **Detail expansion:** Elaborating on existing elements with vivid descriptions of lighting, textures, minor objects, background elements, character attire details, and environmental subtleties.\n"
            "* **Mood/Emotion adjustment:** Subtly modifying descriptions of lighting, color, character expressions, and environmental details to reflect a desired mood (e.g., 'eerie', 'joyful', 'tense') while keeping the core subject and action.\n"
            "* **Attribute changes:** Precisely changing specific attributes like 'characters', 'setting', 'story', or 'style'.\n"
            "Crucially, ensure the final prompt flows naturally and integrates all elements. Your output must be only the refined prompt, without any extra commentary or conversational filler. Prioritize the user's changes while maintaining a cohesive and natural flow."
        ),
        "next_scene_generator": (
            "You are a creative AI image prompt generator that helps continue a story. "
            "You will receive the 'previous_prompt_text' (the previous image manifestation as plain text). "
            "Your task is to create a *new, cohesive, and highly detailed text prompt* "
            "for an AI image model that logically describes the *next scene* in the narrative. "
            "Crucially, **do not just append to the previous prompt**. Instead, generate a "
            "completely fresh prompt that builds upon the implied conclusion or events "
            "of the `previous_prompt_text`. Consider how characters, setting, and story "
            "elements might evolve. The new prompt should be distinct from the previous one, "
            "showing clear progression. Your output must be only the new refined prompt, "
            "without any extra commentary."
            "make proper continuation for the story, do not append on the previous prompt, just generate the next scene."
        ),
        "rephrase_manifestation_generator": (
            "You are an AI image prompt assistant specializing in **rephrasing** existing prompts. "
            "You will receive the 'prompt_to_rephrase' (the complete previous text prompt as plain text). "
            "Your task is to generate a *new, distinct text prompt* that **only rewords or restructures the language** "
            "of the `prompt_to_rephrase`. **DO NOT change the core elements** such as characters, "
            "setting, story/action, art style, or any advanced details. Focus purely on synonyms, "
            "sentence structure, and descriptive phrasing to offer a fresh linguistic take. "
            "Your output must be only the new rephrased prompt, without any extra commentary."
        ),
        "acknowledgement_responder": (
            "You are a helpful and proactive AI assistant for an image manifestation app. "
            "A user has just provided positive but unspecific feedback (e.g., 'good', 'nice', 'perfect'). "
            "Your task is to acknowledge their positive feedback in a friendly way, "
            "and then immediately offer specific next steps or ask a clarifying question to continue the creative process. "
            "Suggest actions like 'Would you like to refine something specific?', 'Should we generate an image now?', "
            "or 'Do you want to explore a next scene or an alternative story?'. "
            "Keep the response concise and encouraging. Your output should be a conversational sentence or two, without any extra commentary or prompt formatting."
        ),
        "alternative_story_generator": (
            "You are a creative AI image prompt assistant for generating *alternative stories*. "
            "You will receive the following components: 'current_characters', 'current_setting', 'current_style', "
            "and a 'user_specific_request' (e.g., 'give me a new story', 'different take', 'keep characters the same but change the story'). "
            "Your task is to generate a *brand new, cohesive, and highly detailed text prompt* "
            "that creates a **completely different story or action** while explicitly leveraging the 'current_characters', 'current_setting', and 'current_style'. "
            "Crucially, prioritize retaining the specified 'current_characters' unless the user's request explicitly overrides them. "
            "Focus on a fresh narrative or a significant plot twist. "
            "Your output must be only the new alternative prompt, without any extra commentary."
        ),
        "style_blender": (
            "You are an AI image prompt assistant specializing in blending art styles. "
            "You will receive a dictionary with 'user_changes' (e.g., 'blend cyberpunk and impressionistic'). "
            "Your task is to generate a cohesive and creative description of a new art style that intelligently combines elements from the styles mentioned in 'user_changes', "
            "for an AI image model. Ensure the blended style is unique yet harmonious. "
            "Your output must be only the new blended style description, without any extra commentary."
        )
    }

    system_prompt = system_prompts.get(system_role, "You are a helpful assistant.")

    # Prepare user content based on role
    if system_role in ["rephrase_manifestation_generator", "next_scene_generator", "acknowledgement_responder", "style_blender"]:
        final_user_content = {"user_changes": user_manifest}
    elif system_role == "alternative_story_generator":
        final_user_content = user_manifest
    elif system_role == "prompt editor":
        final_user_content = user_manifest
    else:
        final_user_content = {"user_input": user_manifest}

    try:
        response = client.chat(
            model='gemma3:4b',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(final_user_content)}
            ],
            stream=False
        )
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"


def generate_image(prompt):
    """Generate image using the Gemini API."""
    api_key = ""  # Canvas will provide it
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key=${api_key}"
    payload = {
        "instances": {"prompt": prompt},
        "parameters": {"sampleCount": 1}
    }

    try:
        response = st.experimental_rerun_with_retries(
            lambda: json.loads(requests.post(
                api_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload)
            ).content.decode('utf-8')),
            catch_exceptions=True
        )

        if (response and response.get('predictions') and 
            len(response['predictions']) > 0 and 
            response['predictions'][0].get('bytesBase64Encoded')):
            return f"data:image/png;base64,{response['predictions'][0]['bytesBase64Encoded']}"
        else:
            return None
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None