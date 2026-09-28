from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from app.config import get_settings
from app.utils.files import unique_filename

@lru_cache(maxsize=1)
def _load_pipeline():
    import torch
    from diffusers import StableDiffusionPipeline
    s = get_settings(); kwargs = {"use_safetensors": True}
    if s.hf_token: kwargs["token"] = s.hf_token
    if torch.cuda.is_available(): kwargs["torch_dtype"] = torch.float16; device = "cuda"
    elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available(): kwargs["torch_dtype"] = torch.float32; device = "mps"
    else: kwargs["torch_dtype"] = torch.float32; device = "cpu"
    pipe = StableDiffusionPipeline.from_pretrained(s.sd_model_id, **kwargs).to(device)
    if device == "cuda": pipe.enable_attention_slicing()
    return pipe, device

def _placeholder(prompt, path, number):
    s = get_settings(); img = Image.new("RGB", (s.image_width, s.image_height), (244,239,230)); d = ImageDraw.Draw(img); f = ImageFont.load_default()
    d.rectangle((20,20,s.image_width-20,s.image_height-20), outline=(40,40,40), width=4)
    d.text((40,45), f"ComicCraft — Panel {number}", fill=(20,20,20), font=f)
    d.text((40,90), prompt[:500], fill=(30,30,30), font=f); img.save(path)

def generate_image(image_prompt, panel_number, art_style, character_name):
    s = get_settings(); path = s.panels_dir / unique_filename(f"panel_{panel_number}", ".png")
    final = f"{image_prompt}, {art_style} comic illustration, consistent character design for {character_name}, cinematic composition, expressive faces, clean line art, vivid colors, no speech bubbles, no captions, no text, no watermark"
    if not s.enable_image_generation:
        _placeholder(final, path, panel_number); return str(path)
    try:
        pipe, device = _load_pipeline(); generator = None
        try:
            import torch; generator = torch.Generator(device=device).manual_seed(1000 + panel_number)
        except Exception: pass
        result = pipe(prompt=final, negative_prompt="text, letters, words, watermark, logo, blurry, deformed", num_inference_steps=s.image_steps, guidance_scale=s.image_guidance, width=s.image_width, height=s.image_height, generator=generator)
        result.images[0].save(path); return str(path)
    except Exception as exc:
        _placeholder(f"Image generation unavailable: {type(exc).__name__}", path, panel_number); return str(path)
