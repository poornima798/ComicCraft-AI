from pydantic import BaseModel, Field, field_validator

class PromptRequest(BaseModel):
    story_prompt: str = Field(..., min_length=5, max_length=3000)
    character_name: str = Field(..., min_length=1, max_length=80)
    setting: str = Field(..., min_length=1, max_length=120)
    tone: str = Field(..., min_length=1, max_length=80)
    art_style: str = Field(..., min_length=1, max_length=100)

    @field_validator("*")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value: raise ValueError("Value cannot be empty.")
        return value

class PanelOutline(BaseModel):
    panel_number: int = Field(..., ge=1)
    title: str
    scene_description: str
    image_prompt: str

class ComicOutline(BaseModel):
    panels: list[PanelOutline]

class PanelStory(BaseModel):
    panel_number: int = Field(..., ge=1)
    title: str
    scene_description: str
    caption: str
    narration: str
    dialogue: str
    image_prompt: str

class ComicStory(BaseModel):
    panels: list[PanelStory]

class ComicPanel(BaseModel):
    panel_number: int
    title: str
    image_url: str
    image_path: str
    scene_description: str
    caption: str
    narration: str
    dialogue: str
    image_prompt: str

class ComicLayout(BaseModel):
    panels: list[ComicPanel]
    pdf_url: str | None = None
