from pathlib import Path
from datetime import datetime, timezone
from fpdf import FPDF
from app.config import get_settings
from app.utils.files import safe_filename

class ComicPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16); self.cell(0, 10, "ComicCraft", new_x="LMARGIN", new_y="NEXT", align="C"); self.ln(2)

def _text(pdf, label, value):
    pdf.set_font("Helvetica", "B", 11); pdf.multi_cell(0, 7, label); pdf.set_font("Helvetica", "", 11); pdf.multi_cell(0, 6, value); pdf.ln(2)

def save_pdf(layout, title="ComicCraft Comic"):
    s = get_settings(); stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"); path = s.exports_dir / f"{safe_filename(title,35)}_{stamp}.pdf"
    pdf = ComicPDF(format="A4"); pdf.set_auto_page_break(auto=True, margin=14)
    for panel in layout["panels"]:
        pdf.add_page(); pdf.set_font("Helvetica", "B", 16); pdf.multi_cell(0, 10, f"Panel {panel['panel_number']}: {panel['title']}", align="C"); pdf.ln(2)
        image = Path(panel["image_path"])
        if image.exists(): pdf.image(str(image), x=20, w=170); pdf.ln(4)
        _text(pdf, "Scene", panel["scene_description"]); _text(pdf, "Caption", panel["caption"]); _text(pdf, "Narration", panel["narration"])
        if panel.get("dialogue"): _text(pdf, "Dialogue", panel["dialogue"])
    pdf.output(str(path)); return str(path)
