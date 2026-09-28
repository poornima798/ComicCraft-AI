import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings(BaseModel):
    app_name: str = "ComicCraft"
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_flash_model: str = Field(default_factory=lambda: os.getenv("GEMINI_FLASH_MODEL", "gemini-2.5-flash"))
    gemini_pro_model: str = Field(default_factory=lambda: os.getenv("GEMINI_PRO_MODEL", "gemini-2.5-pro"))
    hf_token: str = Field(default_factory=lambda: os.getenv("HF_TOKEN", ""))
    sd_model_id: str = Field(default_factory=lambda: os.getenv("SD_MODEL_ID", "stable-diffusion-v1-5/stable-diffusion-v1-5"))
    enable_image_generation: bool = Field(default_factory=lambda: os.getenv("ENABLE_IMAGE_GENERATION", "1").lower() in {"1","true","yes","on"})
    num_panels: int = Field(default_factory=lambda: int(os.getenv("NUM_PANELS", "5")), ge=1, le=10)
    image_steps: int = Field(default_factory=lambda: int(os.getenv("IMAGE_STEPS", "25")), ge=1, le=100)
    image_guidance: float = Field(default_factory=lambda: float(os.getenv("IMAGE_GUIDANCE", "7.5")), gt=0)
    image_width: int = Field(default_factory=lambda: int(os.getenv("IMAGE_WIDTH", "512")), ge=256, le=1024)
    image_height: int = Field(default_factory=lambda: int(os.getenv("IMAGE_HEIGHT", "512")), ge=256, le=1024)
    static_dir: Path = BASE_DIR / "static"
    template_dir: Path = BASE_DIR / "templates"
    panels_dir: Path = BASE_DIR / "static" / "panels"
    exports_dir: Path = BASE_DIR / "static" / "exports"

@lru_cache
def get_settings() -> Settings:
    s = Settings()
    s.panels_dir.mkdir(parents=True, exist_ok=True)
    s.exports_dir.mkdir(parents=True, exist_ok=True)
    return s
