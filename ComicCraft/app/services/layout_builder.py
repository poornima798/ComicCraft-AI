from pathlib import Path
from app.models import ComicPanel, ComicLayout

def build_comic_layout(story, image_paths):
    if len(story) != len(image_paths): raise ValueError("Every story panel must have one image.")
    panels = []
    for item, image_path in zip(story, image_paths):
        p = Path(image_path)
        panels.append(ComicPanel(panel_number=item["panel_number"], title=item["title"], image_url=f"/static/panels/{p.name}", image_path=str(p), scene_description=item["scene_description"], caption=item["caption"], narration=item["narration"], dialogue=item["dialogue"], image_prompt=item["image_prompt"]))
    return ComicLayout(panels=panels).model_dump()
