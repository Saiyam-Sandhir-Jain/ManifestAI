import os

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_EMBED_MODEL = "mxbai-embed-large:latest"

# UI Constants
SIMILARITY_THRESHOLD = 0.45

# Role descriptions for embedding-based matching
ROLE_DESCRIPTIONS = {
    "prompt editor": (
        "edit, refine, modify, change, shorten, lengthen, simplify, expand, "
        "adjust mood, alter lighting, alter textures, alter props, "
        "alter setting, alter style, alter characters, alter story, "
        "regenerate, replace, swap, remove, delete, make, turn, convert, "
        "add, insert, update, revise, rework, tune, tweak, "
        "change the character to, make the setting, add a, remove the, "
        "replace the with, turn the into, change the time of day, "
        "adjust the camera angle, add more detail, make it more descriptive, "
        "change the mood to, make it more cinematic, make it more dramatic, "
        "in the style of, "
        "fix this, it's not working, there's an error, the code is broken, "
        "create a character, add a new protagonist, invent a sidekick, design a villain, "
        "keep the character but change the setting, keep the setting but change the characters, "
        "keep the style but change the subject, replace the main character, "
        "change X but keep Y, replace X with Y, replace A with B, swap A for B, "
    ),
    "next_scene_generator": (
        "next scene, what happens next, continue story, advance narrative, plot progression, "
        "continue"
        "next part of the story, aftermath of, jump forward, move on, next chapter, "
        "show the next logical step, "
        "next, continue, advance, proceed, afterwards, then, finally, eventually, "
        "cut to, dissolve, flash forward, transition, "
    ),
    "rephrase_manifestation_generator": (
        "rephrase, reword, paraphrase, rewrite, re-express, "
        "summarize the story, provide a synopsis, create a summary, "
        "put this in other words, rewrite in a humorous tone, give me a professional version, "
        "simplify, clarify, explain this in simple terms, "
        "make this more concise, condense this, what's the core message, "
        "change the tone of this, make this sound more, "
        "in a nutshell, what's the gist of this, what's the main takeaway, "
    ),
    "acknowledgement_responder": (
        "good, great, excellent, awesome, perfect, superb, fantastic, cool, wonderful, "
        "love it, nailed it, spot on, exactly, that's it, that's the one, this works, "
        "thanks, thank you, got it, okay, alright, sounds good, makes sense, "
        "understood, affirmative, confirmed, "
        "yes, yep, on point, that's right, "
        "that's perfect, works for me, noted, "
    ),
    "alternative_story_generator": (
        "alternative story, new story, different take, another plot, different scenario, different version, "
        "make another with same characters, new plot with existing elements, "
        "keep the characters but change the story, completely change the plot, "
        "what if the story was different, reimagine the story, give them a new adventure, "
        "change, remix, twist, reboot, spin, alternate, "
        "what if the villain was the hero, "
        "retell the tale from a different point of view, put the characters in a new genre, "
    ),
    "style_blender": (
        "blend styles, mix styles, combine art, fusion of styles, merge aesthetics, "
        "blend A and B, mashup of, combine the styles of, in the style of, hybrid style, "
        "Impressionism, Surrealism, Abstract, Pop Art, Futurism, Steampunk, Cyberpunk, "
        "Watercolor, Oil painting, Charcoal sketch, Manga, Anime, Comic book art, "
        "Art Deco, Bauhaus, Brutalism, Gothic, "
        "collage, pastiche, homage, tribute, synthesize, hybridize, amalgamate, fuse, crossover, "
        "retro, futuristic, noir, surreal, abstract, impressionistic, "
        "photorealism, hyperrealism, rococo, dadaism, art nouveau, expressionist, romanticist, "
        "street art, graffiti, mural, fresco, sketch, doodling, digital painting, "
    ),
}