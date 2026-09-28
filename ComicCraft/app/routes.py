from pathlib import Path
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.config import get_settings
from app.models import PromptRequest
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf

router = APIRouter(); settings = get_settings(); templates = Jinja2Templates(directory=str(settings.template_dir))

def run_comic_generation(payload):
    outline = generate_outline(payload.story_prompt, payload.character_name, payload.setting, payload.tone, payload.art_style)
    story = generate_story(outline, payload.character_name, payload.setting, payload.tone, payload.art_style)
    images = [generate_image(p["image_prompt"], p["panel_number"], payload.art_style, payload.character_name) for p in story]
    layout = build_comic_layout(story, images); pdf = save_pdf(layout, f"{payload.character_name}_comic"); layout["pdf_url"] = f"/static/exports/{Path(pdf).name}"; return layout

@router.get("/", response_class=HTMLResponse)
async def home(request: Request): return templates.TemplateResponse(request=request, name="index.html", context={})

@router.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, story_prompt: str = Form(...), character_name: str = Form(...), setting: str = Form(...), tone: str = Form(...), art_style: str = Form(...)):
    try:
        p = PromptRequest(story_prompt=story_prompt, character_name=character_name, setting=setting, tone=tone, art_style=art_style)
        layout = run_comic_generation(p); return templates.TemplateResponse(request=request, name="comic_preview.html", context={"layout": layout, "character_name": p.character_name})
    except Exception as exc:
        return templates.TemplateResponse(request=request, name="error.html", context={"message": str(exc)}, status_code=500)

@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    try: return JSONResponse(content=run_comic_generation(payload))
    except Exception as exc: raise HTTPException(status_code=500, detail=str(exc)) from exc

@router.get("/test-image")
async def test_image(prompt: str = "a brave fox in an enchanted forest"):
    try:
        p = generate_image(prompt, 0, "comic book", "Test Character"); return {"message":"Image generated successfully.", "image_url":f"/static/panels/{Path(p).name}"}
    except Exception as exc: raise HTTPException(status_code=500, detail=str(exc)) from exc

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_url: str | None = None): return templates.TemplateResponse(request=request, name="export_success.html", context={"pdf_url": pdf_url})
