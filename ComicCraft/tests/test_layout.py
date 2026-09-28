from app.services.layout_builder import build_comic_layout

def test_build_comic_layout():
    story=[{"panel_number":1,"title":"Door","scene_description":"Fox finds a door.","caption":"Deep in the woods...","narration":"Fenn steps closer.","dialogue":"Hello?","image_prompt":"fox at hidden door"}]
    result=build_comic_layout(story,["/tmp/panel.png"])
    assert len(result["panels"])==1
    assert result["panels"][0]["image_url"].startswith("/static/panels/")
