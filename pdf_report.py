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
from questions import ORDER
from recommendations import COMMON_ROUTINE_NOTE, RECOMMENDATIONS
from tracks import TRACKS

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


def goal_section(track: str, goal: str, level_key: str) -> list:
    """Блок рекомендаций под цель ученика (ОГЭ/ЕГЭ, работа, путешествия и т. д.)."""
    module = TRACKS[track]
    recs = module.RECS
    story = [Paragraph(escape(recs["title"]), h2)]
    targets = getattr(module, "TARGETS", {})
    for exam, (needed, note) in targets.items():
        if exam in goal:
            if ORDER.index(level_key) >= ORDER.index(needed):
                text = f"{exam}: {note}. Ваш уровень уже подходит, теперь главное — формат экзамена и стратегия."
            else:
                text = f"{exam}: {note}. Сейчас важно подтянуть уровень и параллельно привыкать к формату заданий."
            story += [Paragraph(escape(text), base), Spacer(1, 4)]
    story.append(bullets(recs["tips"]))
    if recs.get("resources"):
        story += [Spacer(1, 4), Paragraph("Материалы под вашу цель:", base), bullets(recs["resources"])]
    return story


def build_pdf(level_key: str, level_title: str, description: str, user_name: str,
              track: str = "general", goal: str = "", parts: dict = None) -> bytes:
    rec = RECOMMENDATIONS[level_key]
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm,
                            title=f"Как учить английский: {level_title}", author=config.TEACHER_NAME)
    story = [
        Paragraph("Как учить английский на вашем уровне", h1),
        Spacer(1, 4),
        Paragraph((f"Для: {escape(user_name)} · " if user_name else "") + f"уровень <b>{escape(level_title)}</b>"
                  + (f" · цель: {escape(goal)}" if goal else ""), base),
        Spacer(1, 6),
        Paragraph(escape(description), base),
        *([Spacer(1, 4), Paragraph(escape(" · ".join(f"{k}: {v}" for k, v in parts.items())), small)]
          if parts else []),
        *goal_section(track, goal, level_key),
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
