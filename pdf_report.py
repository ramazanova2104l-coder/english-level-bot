from functools import lru_cache
from io import BytesIO
from xml.sax.saxutils import escape

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import brand
import config
from questions import ORDER
from recommendations import COMMON_ROUTINE_NOTE, RECOMMENDATIONS, SKILL_MEANING
from vocabulary import VOCAB
from tracks import TRACKS

# Фирменный стиль @ramazanova_eng: журнальная система из brand.py
CREAM = colors.HexColor(brand.CREAM)          # фон страницы
PAPER = colors.HexColor(brand.PAPER)          # бумажные карточки
BURGUNDY = colors.HexColor(brand.BURGUNDY)    # обложка, плашки уровней, блок с промокодом
BLACK = colors.HexColor(brand.BLACK)          # заголовки и текст
WARM_GRAY = colors.HexColor(brand.WARM_GRAY)  # подписи, тонкие линии
ESPRESSO = colors.HexColor(brand.ESPRESSO)    # пояснения
PETAL = colors.HexColor(brand.PETAL)          # редкие розовые акценты
BEIGE = colors.HexColor(brand.BEIGE)          # скотч, подложки, разделители

for name, file in [("Manrope", brand.SANS), ("Manrope-Medium", brand.SANS_MED),
                   ("Manrope-SemiBold", brand.SANS_SEMI), ("Manrope-Bold", brand.SANS_BOLD),
                   ("Playfair", brand.DISPLAY), ("Playfair-SemiBold", brand.DISPLAY_BOLD),
                   ("Playfair-Italic", brand.ITALIC), ("Playfair-MediumItalic", brand.ITALIC_MED),
                   ("Oswald", brand.NARROW)]:
    pdfmetrics.registerFont(TTFont(name, str(brand.FONTS / file)))
pdfmetrics.registerFontFamily("Manrope", normal="Manrope", bold="Manrope-SemiBold",
                              italic="Manrope", boldItalic="Manrope-SemiBold")
pdfmetrics.registerFontFamily("Playfair", normal="Playfair", bold="Playfair-SemiBold",
                              italic="Playfair-Italic", boldItalic="Playfair-MediumItalic")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN
TOP = 16 * mm
BAND_H = 88 * mm   # бордовая обложка на первой странице
OVERLAP = 20 * mm  # насколько карточка с уровнем заходит на обложку

text = ParagraphStyle("text", fontName="Manrope", fontSize=9.5, leading=14.5, textColor=BLACK)
note = ParagraphStyle("note", parent=text, fontSize=8.5, leading=12.5, textColor=ESPRESSO)
lead = ParagraphStyle("lead", parent=text, fontSize=10.5, leading=16)
section_title = ParagraphStyle("section_title", fontName="Playfair", fontSize=17, leading=21, textColor=BLACK)
level_big = ParagraphStyle("level_big", fontName="Playfair-SemiBold", fontSize=64, leading=60, textColor=BURGUNDY)
level_name = ParagraphStyle("level_name", fontName="Playfair-Italic", fontSize=22, leading=26, textColor=BLACK)
skill_value = ParagraphStyle("skill_value", fontName="Playfair-SemiBold", fontSize=26, leading=28,
                             textColor=CREAM, alignment=TA_CENTER)
skill_meaning = ParagraphStyle("skill_meaning", parent=text, fontSize=7.5, leading=10, textColor=CREAM,
                               alignment=TA_CENTER)
cta_title = ParagraphStyle("cta_title", fontName="Playfair", fontSize=22, leading=27, textColor=CREAM,
                           alignment=TA_CENTER)
cta_text = ParagraphStyle("cta_text", parent=text, textColor=CREAM, alignment=TA_CENTER)
cta_sign = ParagraphStyle("cta_sign", fontName="Playfair-Italic", fontSize=11, leading=14, textColor=PETAL,
                          alignment=TA_CENTER)
promo = ParagraphStyle("promo", fontName="Oswald", fontSize=30, leading=34, textColor=BURGUNDY,
                       alignment=TA_CENTER)
promo_note = ParagraphStyle("promo_note", parent=text, fontSize=8.5, leading=12, textColor=ESPRESSO,
                            alignment=TA_CENTER)

SKILL_EN = {"Грамматика и лексика": "GRAMMAR", "Аудирование": "LISTENING", "Чтение": "READING"}


@lru_cache(maxsize=None)
def paper_texture() -> ImageReader:
    """Деликатная текстура бумаги: едва заметное зерно на кремовом."""
    noise = Image.effect_noise((420, 594), 6).point(lambda v: 128 + (v - 128) // 2)
    base = Image.new("RGB", noise.size, brand.CREAM)
    grain = Image.merge("RGB", [noise] * 3)
    return ImageReader(Image.blend(base, grain, 0.06))


class Label(Flowable):
    """Короткая подпись узким шрифтом в разрядку: рубрики, технические надписи."""

    def __init__(self, label, color=BURGUNDY, size=8.5, space=1.6, align="left", font="Oswald"):
        super().__init__()
        self.label, self.color, self.size, self.space, self.align, self.font = label, color, size, space, align, font

    def wrap(self, avail_w, avail_h):
        self.avail_w = avail_w
        return avail_w, self.size + 2

    def draw(self):
        c = self.canv
        c.setFont(self.font, self.size)
        c.setFillColor(self.color)
        w = pdfmetrics.stringWidth(self.label, self.font, self.size) + self.space * (len(self.label) - 1)
        x = {"left": 0, "center": (self.avail_w - w) / 2, "right": self.avail_w - w}[self.align]
        c.drawString(x, 2, self.label, charSpace=self.space)


def tape(c, x, y, w=22 * mm, h=6.5 * mm, angle=-6):
    """Полоска бумажного скотча, как в скрапбуке."""
    c.saveState()
    c.translate(x, y)
    c.rotate(angle)
    c.setFillColor(BEIGE)
    c.setFillAlpha(0.75)
    c.rect(-w / 2, -h / 2, w, h, stroke=0, fill=1)
    c.restoreState()


class PaperCard(Flowable):
    """Лист бумаги поверх второго, чуть повёрнутого листа, сверху кусочек скотча."""

    def __init__(self, content: list, padding=16, tilt=-1.4, tape_at="left"):
        super().__init__()
        self.tilt, self.tape_at = tilt, tape_at
        self.table = Table([[content]], colWidths=[CONTENT_W])
        self.table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PAPER),
            ("BOX", (0, 0), (-1, -1), 0.4, BEIGE),
            ("LEFTPADDING", (0, 0), (-1, -1), padding), ("RIGHTPADDING", (0, 0), (-1, -1), padding),
            ("TOPPADDING", (0, 0), (-1, -1), padding + 2), ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
        ]))

    def wrap(self, avail_w, avail_h):
        self.w, self.h = self.table.wrap(avail_w, avail_h)
        return self.w, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        c.translate(self.w / 2, self.h / 2)
        c.rotate(self.tilt)
        c.setFillColor(BEIGE)
        c.rect(-self.w / 2 + 4, -self.h / 2 - 3, self.w - 6, self.h, stroke=0, fill=1)
        c.restoreState()
        self.table.drawOn(c, 0, 0)
        x = 30 * mm if self.tape_at == "left" else self.w - 30 * mm
        tape(c, x, self.h, angle=-6 if self.tape_at == "left" else 5)


def page_footer(canvas, doc):
    canvas.setStrokeColor(WARM_GRAY)
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN, 13.5 * mm, PAGE_W - MARGIN, 13.5 * mm)
    canvas.setFont("Oswald", 8)
    canvas.setFillColor(WARM_GRAY)
    canvas.drawString(MARGIN, 9 * mm, brand.HANDLE, charSpace=1.4)
    num = f"№ {doc.page:02d}"
    canvas.drawString(PAGE_W - MARGIN - pdfmetrics.stringWidth(num, "Oswald", 8) - 1.4 * (len(num) - 1),
                      9 * mm, num, charSpace=1.4)


def on_page(canvas, doc):
    canvas.saveState()
    canvas.drawImage(paper_texture(), 0, 0, PAGE_W, PAGE_H)
    page_footer(canvas, doc)
    canvas.restoreState()


def cover(who: str):
    """Первая страница: бордовая обложка с заголовком, поверх неё ляжет карточка с уровнем."""

    def draw(canvas, doc):
        on_page(canvas, doc)
        canvas.saveState()
        top = PAGE_H - BAND_H
        canvas.setFillColor(BURGUNDY)
        canvas.rect(0, top, PAGE_W, BAND_H, stroke=0, fill=1)
        canvas.setFillColor(CREAM)
        canvas.setFont("Oswald", 8.5)
        canvas.drawString(MARGIN, PAGE_H - 15 * mm, "ENGLISH LEVEL REPORT", charSpace=1.8)
        right = "PERSONAL PLAN"
        canvas.drawString(PAGE_W - MARGIN - pdfmetrics.stringWidth(right, "Oswald", 8.5) - 1.8 * (len(right) - 1),
                          PAGE_H - 15 * mm, right, charSpace=1.8)
        canvas.setStrokeColor(CREAM)
        canvas.setLineWidth(0.4)
        canvas.line(MARGIN, PAGE_H - 18.5 * mm, PAGE_W - MARGIN, PAGE_H - 18.5 * mm)
        canvas.setFont("Playfair", 34)
        canvas.drawString(MARGIN, PAGE_H - 34 * mm, "Как учить английский")
        canvas.setFillColor(PETAL)
        canvas.setFont("Playfair-Italic", 34)
        canvas.drawString(MARGIN, PAGE_H - 47 * mm, "на твоём уровне")
        canvas.setFillColor(BEIGE)
        canvas.setFont("Manrope", 9)
        canvas.drawString(MARGIN, PAGE_H - 57 * mm, who)
        canvas.restoreState()

    return draw


def bullets(items, marker_color=BURGUNDY, marker="•") -> list:
    """Пункты списка отдельными абзацами, чтобы длинный раздел мог перейти на следующую страницу."""
    style = ParagraphStyle(f"bullet_{marker}_{marker_color}", parent=text, leftIndent=14, bulletIndent=0,
                           bulletFontName="Manrope-SemiBold", bulletFontSize=10 if marker == "•" else 9,
                           bulletColor=marker_color, spaceAfter=3)
    return [Paragraph(escape(i), style, bulletText=marker) for i in items]


def rubric(number: int, en: str) -> Table:
    """Шапка раздела: тонкая линия, номер курсивом и рубрика в разрядку."""
    t = Table([[Paragraph(f"{number:02d}", ParagraphStyle("num", fontName="Playfair-Italic", fontSize=13,
                                                         leading=14, textColor=BURGUNDY)),
                Label(en, size=8.5)]],
              colWidths=[11 * mm, None])
    t.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 0.6, BLACK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def section(number: int, en: str, ru: str, body: list, paper=False) -> list:
    head = [rubric(number, en), Spacer(1, 6), Paragraph(escape(ru), section_title), Spacer(1, 6)]
    if paper:
        return [KeepTogether([*head, Spacer(1, 6), PaperCard(body, padding=14, tape_at="right"), Spacer(1, 18)])]
    for f in head:  # шапка раздела не остаётся одна внизу страницы
        f.keepWithNext = True
    return [*head, *body, Spacer(1, 16)]


def skills_row(parts: dict) -> Table:
    cells = [[Label(SKILL_EN.get(k, k.upper()), color=PETAL, size=8, align="center"), Spacer(1, 4),
              Paragraph(escape(v), skill_value), Spacer(1, 3),
              Paragraph(escape(SKILL_MEANING.get(k, {}).get(v, "")), skill_meaning)]
             for k, v in parts.items()]
    gap = 6
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
             ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
             ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9)]
    for i in range(0, len(row), 2):
        style.append(("BACKGROUND", (i, 0), (i, 0), BURGUNDY))
    t.setStyle(TableStyle(style))
    return t


vocab_en = ParagraphStyle("vocab_en", parent=text, fontName="Manrope-SemiBold")
vocab_ru = ParagraphStyle("vocab_ru", parent=text, textColor=ESPRESSO)


def vocab_section(number: int, track: str, level_key: str) -> KeepTogether:
    """Страница с полезной лексикой под цель: базовый набор для A0-A2, продвинутый для B1+."""
    data = VOCAB.get(track, VOCAB["general"])
    advanced = ORDER.index(level_key) >= ORDER.index("B1")
    words = data["advanced" if advanced else "basic"]
    rows = [[Paragraph(escape(en), vocab_en), Paragraph(escape(ru), vocab_ru)] for en, ru in words]
    t = Table(rows, colWidths=[CONTENT_W * 0.52, CONTENT_W * 0.48])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, BEIGE),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    level_note = "фразы для уровня B1 и выше" if advanced else "фразы для уровней A1-A2"
    return KeepTogether([rubric(number, "USEFUL VOCABULARY"), Spacer(1, 6),
                         Paragraph(escape(data["title"]), section_title), Spacer(1, 2),
                         Paragraph(level_note + ". Повторяй их вслух и используй в своей речи.", note),
                         Spacer(1, 6), t, Spacer(1, 18)])


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
    body += bullets(recs["tips"])
    if recs.get("resources"):
        body += [Spacer(1, 8), Paragraph("<b>Материалы под твою цель</b>", text), Spacer(1, 3),
                 *bullets(recs["resources"], ESPRESSO)]
    return body, recs["title"]


def cta_block() -> Table:
    """Финальный блок на бордовом: пробный урок и промокод на кремовом «билете»."""
    ticket = Table([[[Label("YOUR PROMO CODE", color=WARM_GRAY, size=8, align="center"), Spacer(1, 5),
                      Paragraph(escape(config.PROMO_CODE), promo), Spacer(1, 3),
                      Paragraph(escape(config.PROMO_TEXT), promo_note)]]],
                   colWidths=[CONTENT_W * 0.62])
    ticket.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PAPER),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    content = [
        Paragraph(f"with love, {escape(config.TEACHER_NAME)}", cta_sign),
        Spacer(1, 8),
        Paragraph(f"Первый урок с {escape(config.TEACHER_NAME_INSTR)} "
                  f"<font name='Playfair-Italic' color='{brand.PETAL}'>бесплатно</font>", cta_title),
        Spacer(1, 8),
        Paragraph(escape(config.PDF_OFFER_TEXT), cta_text),
        Spacer(1, 14),
        ticket,
        Spacer(1, 14),
        Label(f"INSTAGRAM · {config.INSTAGRAM_URL.replace('https://', '').upper()}", color=BEIGE, size=8,
              align="center"),
    ]
    t = Table([[content]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BURGUNDY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 22), ("RIGHTPADDING", (0, 0), (-1, -1), 22),
        ("TOPPADDING", (0, 0), (-1, -1), 20), ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
    ]))
    return t


def build_pdf(level_key: str, level_title: str, description: str, user_name: str,
              track: str = "general", goal: str = "", parts: dict = None) -> bytes:
    rec = RECOMMENDATIONS[level_key]
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=TOP, bottomMargin=20 * mm,
                            title=f"Как учить английский: {level_title}", author=config.TEACHER_NAME)
    code = level_key if level_key != "A0" else "A0-A1"
    name = level_title.split(" (")[0]
    who = (f"{user_name}, " if user_name else "") + "это твой персональный план"
    if goal:
        who += f" · цель: {goal}"

    level_card = PaperCard([
        Label("YOUR LEVEL", size=8),
        Spacer(1, 6),
        Table([[Paragraph(escape(code), level_big), Paragraph(escape(name), level_name)]],
              colWidths=[48 * mm, CONTENT_W - 48 * mm - 36],
              style=[("VALIGN", (0, 0), (-1, -1), "BOTTOM"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                     ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]),
        Spacer(1, 6),
        Paragraph(escape(description), lead),
    ], padding=18)
    story = [Spacer(1, BAND_H - TOP - OVERLAP), level_card, Spacer(1, 14)]
    if parts:
        story += [skills_row(parts), Spacer(1, 22)]

    body, title = goal_body(track, goal, level_key)
    story += [
        *section(1, "YOUR GOAL", title, body),
        *section(2, "FOCUS", "На чём сосредоточиться", bullets(rec["focus"])),
        *section(3, "DAILY PLAN", "План на день: 20-30 минут", [*bullets(rec["routine"]), Spacer(1, 4),
                                                                 Paragraph(escape(COMMON_ROUTINE_NOTE), note)],
                 paper=True),
        *section(4, "RESOURCES", "Полезные материалы", bullets(rec["resources"])),
        *section(5, "MISTAKES", "Частые ошибки на этом уровне", bullets(rec["mistakes"], marker="×")),
        vocab_section(6, track, level_key),
        KeepTogether([cta_block()]),
    ]
    doc.build(story, onFirstPage=cover(who), onLaterPages=on_page)
    return buf.getvalue()
