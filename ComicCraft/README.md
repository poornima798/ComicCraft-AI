# ComicCraft — AI Comic Story Creator

FastAPI + Jinja2 application implementing the supplied ComicCraft workflow: five-panel Gemini outline, Gemini story/dialogue, Stable Diffusion illustration, panel layout and multi-page PDF export.

## Installation

Python 3.11 is recommended.

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Put your Gemini key in `.env`:

```env
GEMINI_API_KEY=YOUR_KEY
```

Run:

```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 and API docs at http://127.0.0.1:8000/docs.

## No-GPU development

Set `ENABLE_IMAGE_GENERATION=0`. The app creates placeholder PNGs, so the complete route/layout/PDF workflow can be tested without loading Stable Diffusion.

## Structure

```text
ComicCraft/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── services/
│   │   ├── gemini_flash.py
│   │   ├── gemini_pro.py
│   │   ├── image_generator.py
│   │   ├── layout_builder.py
│   │   └── exporters.py
│   └── utils/files.py
├── templates/
├── static/css/style.css
├── static/js/app.js
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

The supplied document used `google-generativeai`; this implementation uses the current `google-genai` SDK and structured Pydantic responses. Local image generation uses Hugging Face Diffusers. If local diffusion is unavailable, the generator falls back to a placeholder image instead of crashing the web request.
