from google import genai
from google.genai import types
from app.config import get_settings
from app.models import ComicOutline

def generate_outline(story_prompt, character_name, setting, tone, art_style):
    s = get_settings()
    if not s.gemini_api_key: raise RuntimeError("GEMINI_API_KEY is not configured. Add it to .env.")
    prompt = f"""Create exactly {s.num_panels} connected comic panels.
Story: {story_prompt}
Character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}
For every panel return a concise title, visual scene description, and a detailed image-generation prompt. Keep the same character identity and plot continuity. Do not include text or speech bubbles in image prompts."""
    # Create the client on its own line first
    client = genai.Client(api_key=s.gemini_api_key)

    response = client.models.generate_content(
    model=s.gemini_flash_model,
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json", 
        response_schema=ComicOutline
    )
)
    if not response.text: raise RuntimeError("Gemini returned an empty outline.")
    result = ComicOutline.model_validate_json(response.text)
    if len(result.panels) != s.num_panels: raise RuntimeError(f"Expected {s.num_panels} panels, got {len(result.panels)}.")
    return [p.model_dump() for p in result.panels]
