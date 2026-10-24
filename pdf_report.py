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
from vocabulary import VOCAB
from tracks import TRACKS

import brand

# Фирменный стиль @ramazanova_eng (цвета и шрифты в brand.py)
IVORY = colors.HexColor(brand.IVORY)        # фон страницы
PAPER = colors.HexColor(brand.PAPER)        # карточки
PEONY = colors.HexColor(brand.PEONY)        # пилюли-рубрики и акцентные плашки
WINE = colors.HexColor(brand.WINE)          # маркеры и рукописные подписи
ESPRESSO = colors.HexColor(brand.ESPRESSO)  # заголовки, текст, тёмные блоки
MUTED = colors.HexColor(brand.MUTED)        # подписи, ник

for name, file in [("Montserrat", brand.SANS), ("Montserrat-Medium", brand.SANS_MED),
                   ("Montserrat-SemiBold", brand.SANS_SEMI), ("Montserrat-Bold", brand.SANS_BOLD),
                   ("Playfair", brand.SERIF), ("Playfair-Italic", brand.SERIF_ITALIC),
                   ("Playfair-SemiItalic", brand.SERIF_ITALIC_SEMI), ("Caveat", brand.HAND)]:
    pdfmetrics.registerFont(TTFont(name, str(brand.FONTS / file)))
pdfmetrics.registerFontFamily("Montserrat", normal="Montserrat", bold="Montserrat-SemiBold",
                              italic="Montserrat", boldItalic="Montserrat-SemiBold")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

text = ParagraphStyle("text", fontName="Montserrat", fontSize=9.5, leading=14.5, textColor=ESPRESSO)
note = ParagraphStyle("note", parent=text, fontSize=8.5, leading=12.5, textColor=MUTED)
lead = ParagraphStyle("lead", parent=text, fontSize=10.5, leading=16)
script_title = ParagraphStyle("script_title", fontName="Playfair-Italic", fontSize=16, leading=20,
                              textColor=ESPRESSO)
big_title = ParagraphStyle("big_title", fontName="Playfair-Italic", fontSize=30, leading=35,
                           textColor=colors.HexColor(brand.IVORY))
hand_light = ParagraphStyle("hand_light", fontName="Caveat", fontSize=20, leading=22, textColor=PEONY)
hand_wine = ParagraphStyle("hand_wine", fontName="Caveat", fontSize=19, leading=21, textColor=WINE)
rubric = ParagraphStyle("rubric", fontName="Montserrat-Bold", fontSize=7.5, leading=9, textColor=ESPRESSO)
level_big = ParagraphStyle("level_big", fontName="Playfair", fontSize=58, leading=58, textColor=ESPRESSO)
level_name = ParagraphStyle("level_name", fontName="Playfair-Italic", fontSize=21, leading=25,
                            textColor=ESPRESSO)
skill_label = ParagraphStyle("skill_label", fontName="Montserrat-Bold", fontSize=7.5, leading=9, textColor=ESPRESSO,
                             alignment=TA_CENTER)
skill_value = ParagraphStyle("skill_value", fontName="Playfair", fontSize=24, leading=26, textColor=ESPRESSO,
                             alignment=TA_CENTER)
cta_title = ParagraphStyle("cta_title", fontName="Playfair-Italic", fontSize=22, leading=26,
                           textColor=colors.HexColor(brand.IVORY), alignment=TA_CENTER)
cta_text = ParagraphStyle("cta_text", parent=text, alignment=TA_CENTER, textColor=colors.HexColor(brand.IVORY))
promo = ParagraphStyle("promo", fontName="Playfair", fontSize=28, leading=30, textColor=ESPRESSO,
                       alignment=TA_CENTER)

SKILL_EN = {"Грамматика и лексика": "GRAMMAR", "Аудирование": "LISTENING", "Чтение": "READING"}


def spaced(label: str) -> str:
    """Заглавные буквы с разрядкой, как в рубриках на референсах."""
    return "&nbsp;".join(escape(label.upper()))


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(IVORY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setFont("Montserrat-SemiBold", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 10 * mm, " ".join("@RAMAZANOVA_ENG"))
    canvas.drawRightString(PAGE_W - MARGIN, 10 * mm, f"{doc.page:02d}")
    canvas.restoreState()


def pill(label: str, background=PEONY) -> Table:
    """Пилюля-рубрика: английское слово заглавными с разрядкой на розовом."""
    width = pdfmetrics.stringWidth(" ".join(label.upper()), "Montserrat-Bold", 7.5) + 24
    t = Table([[Paragraph(spaced(label), rubric)]], colWidths=[width], rowHeights=[18])
    t.hAlign = "LEFT"
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("ROUNDEDCORNERS", [9, 9, 9, 9]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def card(content: list, background=PAPER, padding=16, width=CONTENT_W) -> Table:
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("ROUNDEDCORNERS", [14, 14, 14, 14]),
        ("LEFTPADDING", (0, 0), (-1, -1), padding), ("RIGHTPADDING", (0, 0), (-1, -1), padding),
        ("TOPPADDING", (0, 0), (-1, -1), padding - 2), ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
    ]))
    return t


def bullets(items, marker_color=WINE):
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
        style += [("BACKGROUND", (i, 0), (i, 0), PEONY), ("ROUNDEDCORNERS", [12, 12, 12, 12])]
    t.setStyle(TableStyle(style))
    return t


vocab_en = ParagraphStyle("vocab_en", parent=text, fontName="Montserrat-SemiBold")
vocab_ru = ParagraphStyle("vocab_ru", parent=text, textColor=ESPRESSO)


def vocab_section(track: str, level_key: str) -> KeepTogether:
    """Страница с полезной лексикой под цель: базовый набор для A0-A2, продвинутый для B1+."""
    data = VOCAB.get(track, VOCAB["general"])
    advanced = ORDER.index(level_key) >= ORDER.index("B1")
    words = data["advanced" if advanced else "basic"]
    inner = CONTENT_W - 26
    rows = [[Paragraph(escape(en), vocab_en), Paragraph(escape(ru), vocab_ru)] for en, ru in words]
    t = Table(rows, colWidths=[inner * 0.52, inner * 0.48])
    style = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
             ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
             ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8)]
    for i in range(0, len(rows), 2):
        style.append(("BACKGROUND", (0, i), (-1, i), IVORY))
    t.setStyle(TableStyle(style))
    level_note = "фразы для уровня B1 и выше" if advanced else "фразы для уровней A1-A2"
    return KeepTogether([card([pill("USEFUL VOCABULARY"), Spacer(1, 6), Paragraph(escape(data["title"]), script_title),
                               Spacer(1, 2), Paragraph(level_note + ". Повторяй их вслух и используй в своей речи.", note),
                               Spacer(1, 8), t], padding=13),
                         Spacer(1, 7)])


def goal_body(track: str, goal: str, level_key: str) -> list:
    module = TRACKS[track]
    recs = module.RECS
    body = []
    for exam, (needed, target_note) in getattr(module, "TARGETS", {}).items():
        if exam in goal:
            if ORDER.index(level_key) >= ORDER.index(needed):
                msg = f"{exam}: {target_note}. Твой уровень уже подходит, теперь главное - формат экзамена и стратегия."
            else:
                msg = f"{exam}: {target_note}. Сейчас важно подтянуть уровень и параллельно привыкать к формату заданий."
            body += [Paragraph(escape(msg), text), Spacer(1, 6)]
    body.append(bullets(recs["tips"]))
    if recs.get("resources"):
        body += [Spacer(1, 8), Paragraph("<b>Материалы под твою цель</b>", text), Spacer(1, 3),
                 bullets(recs["resources"], MUTED)]
    return body, recs["title"]


def build_pdf(level_key: str, level_title: str, description: str, user_name: str,
              track: str = "general", goal: str = "", parts: dict = None) -> bytes:
    rec = RECOMMENDATIONS[level_key]
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=16 * mm, bottomMargin=18 * mm,
                            title=f"Как учить английский: {level_title}", author=config.TEACHER_NAME)
    code = level_key if level_key != "A0" else "A0-A1"
    name = level_title.split(" (")[0]
    who = (f"{escape(user_name)}, " if user_name else "") + "это твой персональный план"
    goal_line = f" · цель: {escape(goal)}" if goal else ""

    ivory_note = ParagraphStyle("ivory_note", parent=note, textColor=PEONY)
    cover = card([
        pill("YOUR ENGLISH LEVEL"),
        Spacer(1, 14),
        Paragraph("Как учить английский<br/>на твоём уровне", big_title),
        Spacer(1, 4),
        Paragraph("your personal plan", hand_light),
        Spacer(1, 8),
        Paragraph(who + goal_line, ivory_note),
    ], background=ESPRESSO, padding=20)
    story = [
        cover,
        Spacer(1, 10),
        card([Table([[Paragraph(escape(code), level_big), Paragraph(escape(name), level_name)]],
                    colWidths=[52 * mm, CONTENT_W - 52 * mm - 32],
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
        section("DAILY PLAN", "План на день: 20-30 минут", [bullets(rec["routine"]), Spacer(1, 6),
                                                             Paragraph(escape(COMMON_ROUTINE_NOTE), note)]),
        section("RESOURCES", "Полезные материалы", [bullets(rec["resources"])]),
        section("MISTAKES", "Частые ошибки на этом уровне", [bullets(rec["mistakes"], WINE)]),
        vocab_section(track, level_key),
        KeepTogether([card([
            Paragraph(f"Первый урок с {escape(config.TEACHER_NAME_INSTR)} бесплатно", cta_title),
            Spacer(1, 6),
            Paragraph(escape(config.PDF_OFFER_TEXT), cta_text),
            Spacer(1, 10),
            card([Paragraph(spaced("your promo code"), skill_label), Spacer(1, 4),
                  Paragraph(escape(config.PROMO_CODE), promo), Spacer(1, 2),
                  Paragraph(escape(config.PROMO_TEXT), ParagraphStyle("pt", parent=text, alignment=TA_CENTER))],
                 background=PEONY, padding=12, width=CONTENT_W - 36),
            Spacer(1, 10),
            Paragraph(f"Instagram: {escape(config.INSTAGRAM_URL.replace('https://', ''))}", cta_text),
            Spacer(1, 4),
            Paragraph(f"with love, {escape(config.TEACHER_NAME)}",
                      ParagraphStyle("sig", parent=hand_light, alignment=TA_CENTER)),
        ], background=ESPRESSO, padding=18)]),
    ]
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return buf.getvalue()
