from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.routes import router

@asynccontextmanager
async def lifespan(app):
    s = get_settings(); s.panels_dir.mkdir(parents=True, exist_ok=True); s.exports_dir.mkdir(parents=True, exist_ok=True); yield

s = get_settings(); app = FastAPI(title="ComicCraft API", description="AI Comic Story Creator using Gemini and Stable Diffusion", version="1.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(s.static_dir)), name="static"); app.include_router(router)

@app.get("/health")
async def health(): return {"status":"ok", "service":s.app_name, "image_generation_enabled":s.enable_image_generation}
