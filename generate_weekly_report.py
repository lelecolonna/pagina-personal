"""
Generates a branded weekly market PDF report matching the site's
navy/gold visual identity, and drops it into reports/.

Usage: python3 generate_weekly_report.py
Edit the CONTENT block below each week (or have the automation fill it in).
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, HRFlowable
from reportlab.pdfgen import canvas

# ─── BRAND COLORS (matches index.html :root variables) ───────────
NAVY   = HexColor('#0a1628')
GOLD   = HexColor('#c9a84c')
LIGHT  = HexColor('#f5f5f0')
MUTED  = HexColor('#8a8a8a')
BODY_TEXT = HexColor('#333333')

HEADER_H = 1.35 * inch
FOOTER_H = 0.6 * inch

# ─── CONTENT (update weekly) ──────────────────────────────────────
CONTENT = {
    "tag": "ANÁLISIS DE MERCADOS",
    "title": "Resumen Semanal de Mercados",
    "period": "Semana del 31 de agosto al 4 de septiembre, 2026",
    "published": "Publicado el 7 de septiembre, 2026",
    "body": (
        "La semana del 31 de agosto al 4 de septiembre cerró mixta: el S&amp;P "
        "500 sumó apenas 0.1%, el Nasdaq avanzó 0.4% y el Dow cedió 0.3%, "
        "arrastrado por una caída del 0.5% el viernes tras un reporte de empleo "
        "de agosto muy superior a lo esperado (162,000 nóminas frente a ~55,000 "
        "previstas), que elevó a 58% la probabilidad de una subida de tasas en "
        "la Fed del 15-16 de septiembre. Los rendimientos del Tesoro subieron y "
        "Tesla se desplomó más de 6% tras el debut de su Cybercab. Tom Lee de "
        "Fundstrat mantiene una postura contraria, ve el pesimismo generalizado "
        "como señal alcista y espera que la Fed termine pausando."
    ),
    "sources": "Fuentes: Fundstrat / FS Insight · Bloomberg · MarketWatch",
    "filename": "weekly-2026-09-07.pdf",
}


def draw_static(c: canvas.Canvas, doc):
    width, height = letter

    # Header bar
    c.setFillColor(NAVY)
    c.rect(0, height - HEADER_H, width, HEADER_H, fill=1, stroke=0)

    # Logo mark
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(0.75 * inch, height - 0.55 * inch, "AC")

    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica", 15)
    c.drawString(1.3 * inch, height - 0.53 * inch, "Alessandro Colonna")

    c.setFillColor(GOLD)
    c.setFont("Helvetica", 8)
    c.drawString(1.3 * inch, height - 0.72 * inch, "F I N A N Z A S   &   I N V E R S I O N E S")

    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 0.75 * inch, height - 0.55 * inch, "alessandro@domusinvestments.es")
    c.setFillColor(GOLD)
    c.drawRightString(width - 0.75 * inch, height - 0.72 * inch, "linkedin.com/in/alessandro-colonna-urdaneta")

    # thin gold rule under header
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(0, height - HEADER_H, width, height - HEADER_H)

    # Footer
    c.setFillColor(NAVY)
    c.rect(0, 0, width, FOOTER_H, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    c.setFillColorRGB(1, 1, 1, alpha=0.35)
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(width / 2, FOOTER_H / 2 - 3, "© 2026 Alessandro Colonna · Reporte generado automáticamente cada lunes")


def build(content, out_path):
    width, height = letter
    doc = BaseDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=HEADER_H + 0.45 * inch,
        bottomMargin=FOOTER_H + 0.45 * inch,
    )

    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        id='body', showBoundary=0,
    )
    doc.addPageTemplates([PageTemplate(id='branded', frames=[frame], onPage=draw_static)])

    styles = {
        'tag': ParagraphStyle('tag', fontName='Helvetica-Bold', fontSize=8.5,
                               textColor=GOLD, leading=11, spaceAfter=6, tracking=1),
        'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=22,
                                 textColor=NAVY, leading=26, spaceAfter=4),
        'meta': ParagraphStyle('meta', fontName='Helvetica', fontSize=10,
                                textColor=MUTED, leading=14, spaceAfter=2),
        'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10.5,
                                textColor=BODY_TEXT, leading=17, spaceBefore=16,
                                spaceAfter=14, alignment=TA_JUSTIFY),
        'sources': ParagraphStyle('sources', fontName='Helvetica-Oblique', fontSize=9,
                                   textColor=MUTED, leading=13),
    }

    story = []
    story.append(Paragraph(content['tag'], styles['tag']))
    story.append(Paragraph(content['title'], styles['title']))
    story.append(Paragraph(content['period'], styles['meta']))
    story.append(Paragraph(content['published'], styles['meta']))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceBefore=14, spaceAfter=0))
    story.append(Paragraph(content['body'], styles['body']))
    story.append(HRFlowable(width="35%", thickness=0.75, color=HexColor('#dddddd'),
                             spaceBefore=6, spaceAfter=10, hAlign='LEFT'))
    story.append(Paragraph(content['sources'], styles['sources']))

    doc.build(story)
    return out_path


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, CONTENT["filename"])
    build(CONTENT, out_path)
    print("Generated:", out_path)
