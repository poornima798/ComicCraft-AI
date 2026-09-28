from google import genai
from google.genai import types
from app.config import get_settings
from app.models import ComicStory

def generate_story(outline, character_name, setting, tone, art_style):
    s = get_settings()
    if not s.gemini_api_key: raise RuntimeError("GEMINI_API_KEY is not configured. Add it to .env.")
    outline_text = "\n".join(f"Panel {p['panel_number']}: {p['title']}\nScene: {p['scene_description']}\nImage: {p['image_prompt']}" for p in outline)
    prompt = f"""Expand this outline into exactly {s.num_panels} polished comic panels.
Character: {character_name}; setting: {setting}; tone: {tone}; art style: {art_style}.
Return caption, 1-3 sentence narration, concise dialogue (empty if unnecessary), and an improved image prompt for each panel. Preserve continuity and do not put written text into image prompts.
OUTLINE:\n{outline_text}"""
    # Create the client on its own line first
    client = genai.Client(api_key=s.gemini_api_key)

    response = client.models.generate_content(
    model=s.gemini_pro_model,
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json", 
        response_schema=ComicStory
    )
)
    if not response.text: raise RuntimeError("Gemini returned an empty story.")
    result = ComicStory.model_validate_json(response.text)
    if len(result.panels) != s.num_panels: raise RuntimeError(f"Expected {s.num_panels} story panels, got {len(result.panels)}.")
    return [p.model_dump() for p in result.panels]
