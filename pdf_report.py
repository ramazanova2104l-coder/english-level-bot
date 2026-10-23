from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import config
from recommendations import COMMON_ROUTINE_NOTE, RECOMMENDATIONS

FONTS = Path(__file__).with_name("fonts")
pdfmetrics.registerFont(TTFont("DejaVu", str(FONTS / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(FONTS / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu", boldItalic="DejaVu-Bold")

ACCENT = colors.HexColor("#2F5D8A")
SOFT = colors.HexColor("#EEF3F8")

base = ParagraphStyle("base", fontName="DejaVu", fontSize=10.5, leading=15)
h1 = ParagraphStyle("h1", parent=base, fontName="DejaVu-Bold", fontSize=20, leading=25, textColor=ACCENT)
h2 = ParagraphStyle("h2", parent=base, fontName="DejaVu-Bold", fontSize=13, leading=18,
                    textColor=ACCENT, spaceBefore=10, spaceAfter=4)
small = ParagraphStyle("small", parent=base, fontSize=9, textColor=colors.grey)
center = ParagraphStyle("center", parent=base, alignment=TA_CENTER)


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(escape(i), base), leftIndent=12) for i in items],
        bulletType="bullet", bulletColor=ACCENT, leftIndent=12,
    )


def box(paragraphs):
    t = Table([[paragraphs]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 1, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def build_pdf(level_key: str, level_title: str, description: str, user_name: str) -> bytes:
    rec = RECOMMENDATIONS[level_key]
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm,
                            title=f"Как учить английский: {level_title}", author=config.TEACHER_NAME)
    story = [
        Paragraph("Как учить английский на вашем уровне", h1),
        Spacer(1, 4),
        Paragraph(f"Для: {escape(user_name)} · уровень <b>{escape(level_title)}</b>", base),
        Spacer(1, 6),
        Paragraph(escape(description), base),
        Paragraph("На чём сосредоточиться", h2), bullets(rec["focus"]),
        Paragraph("План на день (20–30 минут)", h2), bullets(rec["routine"]),
        Spacer(1, 4), Paragraph(escape(COMMON_ROUTINE_NOTE), small),
        Paragraph("Полезные материалы", h2), bullets(rec["resources"]),
        Paragraph("Частые ошибки на этом уровне", h2), bullets(rec["mistakes"]),
        Spacer(1, 14),
        box([
            Paragraph(f"<b>Первый урок с {escape(config.TEACHER_NAME_INSTR)} бесплатно</b>", center),
            Spacer(1, 4),
            Paragraph(escape(config.PDF_OFFER_TEXT), center),
            Spacer(1, 6),
            Paragraph(f"Ваш промокод: <b>{escape(config.PROMO_CODE)}</b> ({escape(config.PROMO_TEXT)})", center),
            Spacer(1, 4),
            Paragraph(f"Instagram: {escape(config.INSTAGRAM_URL.replace('https://', ''))}", center),
        ]),
    ]
    doc.build(story)
    return buf.getvalue()
