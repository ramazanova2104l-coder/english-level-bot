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
from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

import config
from questions import ORDER
from recommendations import COMMON_ROUTINE_NOTE, RECOMMENDATIONS
from tracks import TRACKS

# Фирменный стиль @ramazanova_eng (как в визуальной системе публикаций)
CREAM = colors.HexColor("#F8F2EE")      # фон страницы
IVORY = colors.HexColor("#FFFDFB")      # карточки
ROSE = colors.HexColor("#D99BB3")       # пилюли-рубрики и акцентная плашка
SAGE = colors.HexColor("#A6AD96")       # маркеры, «правильно»
CHOCOLATE = colors.HexColor("#42291F")  # заголовки и текст
TAUPE = colors.HexColor("#A69B94")      # подписи, ник

FONTS = Path(__file__).with_name("fonts")
for name, file in [("Montserrat", "Montserrat_400Regular.ttf"), ("Montserrat-Medium", "Montserrat_500Medium.ttf"),
                   ("Montserrat-SemiBold", "Montserrat_600SemiBold.ttf"),
                   ("Cormorant", "CormorantGaramond_500Medium_Italic.ttf"),
                   ("Cormorant-SemiBold", "CormorantGaramond_600SemiBold_Italic.ttf"),
                   ("Bebas", "BebasNeue_400Regular.ttf")]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / file)))
pdfmetrics.registerFontFamily("Montserrat", normal="Montserrat", bold="Montserrat-SemiBold",
                              italic="Montserrat", boldItalic="Montserrat-SemiBold")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

text = ParagraphStyle("text", fontName="Montserrat", fontSize=9.5, leading=14.5, textColor=CHOCOLATE)
note = ParagraphStyle("note", parent=text, fontSize=8.5, leading=12.5, textColor=TAUPE)
lead = ParagraphStyle("lead", parent=text, fontSize=10.5, leading=16)
script_title = ParagraphStyle("script_title", fontName="Cormorant-SemiBold", fontSize=17, leading=20,
                              textColor=CHOCOLATE)
big_title = ParagraphStyle("big_title", fontName="Cormorant-SemiBold", fontSize=30, leading=33,
                           textColor=CHOCOLATE)
rubric = ParagraphStyle("rubric", fontName="Bebas", fontSize=12, leading=13, textColor=CHOCOLATE)
level_big = ParagraphStyle("level_big", fontName="Bebas", fontSize=64, leading=58, textColor=CHOCOLATE)
level_name = ParagraphStyle("level_name", fontName="Cormorant-SemiBold", fontSize=22, leading=25,
                            textColor=CHOCOLATE)
skill_label = ParagraphStyle("skill_label", fontName="Bebas", fontSize=11, leading=12, textColor=TAUPE,
                             alignment=TA_CENTER)
skill_value = ParagraphStyle("skill_value", fontName="Bebas", fontSize=26, leading=26, textColor=CHOCOLATE,
                             alignment=TA_CENTER)
cta_title = ParagraphStyle("cta_title", fontName="Cormorant-SemiBold", fontSize=22, leading=25,
                           textColor=CHOCOLATE, alignment=TA_CENTER)
cta_text = ParagraphStyle("cta_text", parent=text, alignment=TA_CENTER)
promo = ParagraphStyle("promo", fontName="Bebas", fontSize=30, leading=30, textColor=CHOCOLATE,
                       alignment=TA_CENTER)

SKILL_EN = {"Грамматика и лексика": "GRAMMAR", "Аудирование": "LISTENING", "Чтение": "READING"}


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setFont("Bebas", 10)
    canvas.setFillColor(TAUPE)
    canvas.drawString(MARGIN, 10 * mm, "@RAMAZANOVA_ENG")
    canvas.drawRightString(PAGE_W - MARGIN, 10 * mm, f"{doc.page:02d}")
    canvas.restoreState()


def pill(label: str, background=ROSE) -> Table:
    """Пилюля-рубрика: английское слово Bebas Neue на розовом."""
    width = pdfmetrics.stringWidth(label, "Bebas", 12) + 22
    t = Table([[Paragraph(escape(label), rubric)]], colWidths=[width], rowHeights=[18])
    t.hAlign = "LEFT"
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("ROUNDEDCORNERS", [9, 9, 9, 9]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def card(content: list, background=IVORY, padding=16) -> Table:
    t = Table([[content]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("ROUNDEDCORNERS", [14, 14, 14, 14]),
        ("LEFTPADDING", (0, 0), (-1, -1), padding), ("RIGHTPADDING", (0, 0), (-1, -1), padding),
        ("TOPPADDING", (0, 0), (-1, -1), padding - 2), ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
    ]))
    return t


def bullets(items, marker_color=SAGE):
    return ListFlowable(
        [ListItem(Paragraph(escape(i), text), leftIndent=14, value="•") for i in items],
        bulletType="bullet", start="•", bulletColor=marker_color, bulletFontName="Montserrat-SemiBold",
        bulletFontSize=12, leftIndent=14, bulletOffsetY=1,
    )


def section(en: str, ru: str, body: list) -> KeepTogether:
    return KeepTogether([card([pill(en), Spacer(1, 6), Paragraph(escape(ru), script_title), Spacer(1, 4), *body],
                              padding=13),
                         Spacer(1, 7)])


def skills_row(parts: dict) -> Table:
    cells = [[Paragraph(SKILL_EN.get(k, k.upper()), skill_label), Spacer(1, 3), Paragraph(escape(v), skill_value)]
             for k, v in parts.items()]
    gap = 8
    w = (CONTENT_W - gap * (len(cells) - 1)) / len(cells)
    row, widths = [], []
    for i, c in enumerate(cells):
        if i:
            row.append("")
            widths.append(gap)
        row.append(c)
        widths.append(w)
    t = Table([row], colWidths=widths)
    style = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
             ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 12)]
    for i in range(0, len(row), 2):
        style += [("BACKGROUND", (i, 0), (i, 0), IVORY), ("ROUNDEDCORNERS", [12, 12, 12, 12])]
    t.setStyle(TableStyle(style))
    return t


def goal_body(track: str, goal: str, level_key: str) -> list:
    module = TRACKS[track]
    recs = module.RECS
    body = []
    for exam, (needed, target_note) in getattr(module, "TARGETS", {}).items():
        if exam in goal:
            if ORDER.index(level_key) >= ORDER.index(needed):
                msg = f"{exam}: {target_note}. Ваш уровень уже подходит, теперь главное — формат экзамена и стратегия."
            else:
                msg = f"{exam}: {target_note}. Сейчас важно подтянуть уровень и параллельно привыкать к формату заданий."
            body += [Paragraph(escape(msg), text), Spacer(1, 6)]
    body.append(bullets(recs["tips"]))
    if recs.get("resources"):
        body += [Spacer(1, 8), Paragraph("<b>Материалы под вашу цель</b>", text), Spacer(1, 3),
                 bullets(recs["resources"], TAUPE)]
    return body, recs["title"]


def build_pdf(level_key: str, level_title: str, description: str, user_name: str,
              track: str = "general", goal: str = "", parts: dict = None) -> bytes:
    rec = RECOMMENDATIONS[level_key]
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=16 * mm, bottomMargin=18 * mm,
                            title=f"Как учить английский: {level_title}", author=config.TEACHER_NAME)
    code = level_key if level_key != "A0" else "A0–A1"
    name = level_title.split(" (")[0]
    who = (f"{escape(user_name)}, " if user_name else "") + "это ваш персональный план"
    goal_line = f" · цель: {escape(goal)}" if goal else ""

    story = [
        pill("YOUR ENGLISH LEVEL"),
        Spacer(1, 12),
        Paragraph("Как учить английский<br/>на вашем уровне", big_title),
        Spacer(1, 6),
        Paragraph(who + goal_line, note),
        Spacer(1, 14),
        card([Table([[Paragraph(escape(code), level_big), Paragraph(escape(name), level_name)]],
                    colWidths=[48 * mm, CONTENT_W - 48 * mm - 32],
                    style=[("VALIGN", (0, 0), (-1, -1), "BOTTOM"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]),
              Spacer(1, 8), Paragraph(escape(description), lead)]),
        Spacer(1, 10),
    ]
    if parts:
        story += [skills_row(parts), Spacer(1, 12)]

    body, title = goal_body(track, goal, level_key)
    story += [
        section("YOUR GOAL", title, body),
        section("FOCUS", "На чём сосредоточиться", [bullets(rec["focus"])]),
        section("DAILY PLAN", "План на день: 20–30 минут", [bullets(rec["routine"]), Spacer(1, 6),
                                                             Paragraph(escape(COMMON_ROUTINE_NOTE), note)]),
        section("RESOURCES", "Полезные материалы", [bullets(rec["resources"])]),
        section("MISTAKES", "Частые ошибки на этом уровне", [bullets(rec["mistakes"], ROSE)]),
        KeepTogether([card([
            Paragraph(f"Первый урок с {escape(config.TEACHER_NAME_INSTR)} бесплатно", cta_title),
            Spacer(1, 6),
            Paragraph(escape(config.PDF_OFFER_TEXT), cta_text),
            Spacer(1, 8),
            Paragraph("YOUR PROMO CODE", ParagraphStyle("pl", parent=skill_label, textColor=CHOCOLATE)),
            Spacer(1, 4),
            Paragraph(escape(config.PROMO_CODE), promo),
            Spacer(1, 4),
            Paragraph(escape(config.PROMO_TEXT), cta_text),
            Spacer(1, 10),
            Paragraph(f"Instagram: {escape(config.INSTAGRAM_URL.replace('https://', ''))}", cta_text),
        ], background=ROSE, padding=16)]),
    ]
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return buf.getvalue()
