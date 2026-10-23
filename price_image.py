# Рисует картинки с ценами в фирменном стиле @ramazanova_eng из данных formats.PRICES
from functools import lru_cache
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import config
from formats import PRICES, PROMO_ON_PRICES

FONTS = Path(__file__).with_name("fonts")
CREAM = "#F8F2EE"
IVORY = "#FFFDFB"
ROSE = "#D99BB3"
SAGE = "#A6AD96"
CHOCOLATE = "#42291F"
TAUPE = "#A69B94"

W = 1080
PAD = 72


def font(name: str, size: int):
    return ImageFont.truetype(str(FONTS / name), size)


BEBAS = "BebasNeue_400Regular.ttf"
SERIF = "CormorantGaramond_600SemiBold_Italic.ttf"
SANS = "Montserrat_400Regular.ttf"
SANS_MED = "Montserrat_500Medium.ttf"
SANS_BOLD = "Montserrat_600SemiBold.ttf"


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=fnt) <= width:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def pill(draw, x, y, label, fill=ROSE):
    fnt = font(BEBAS, 34)
    w = draw.textlength(label, font=fnt) + 48
    draw.rounded_rectangle([x, y, x + w, y + 52], radius=26, fill=fill)
    draw.text((x + 24, y + 26), label, font=fnt, fill=CHOCOLATE, anchor="lm")
    return w


def price_text(draw, right, cy, value):
    """Цена: цифры Bebas Neue, значок рубля Montserrat (в Bebas нет ₽)."""
    if value == "0":
        fnt = font(SERIF, 46)
        draw.text((right, cy), "бесплатно", font=fnt, fill=CHOCOLATE, anchor="rm")
        return
    num, rub = font(BEBAS, 64), font(SANS_BOLD, 34)
    rub_w = draw.textlength("₽", font=rub)
    draw.text((right, cy + 4), "₽", font=rub, fill=CHOCOLATE, anchor="rm")
    draw.text((right - rub_w - 10, cy + 4), value, font=num, fill=CHOCOLATE, anchor="rm")


def layout(draw, data, dry=False):
    """Рисует (или только меряет при dry=True) и возвращает итоговую высоту."""
    y = PAD
    if not dry:
        pill(draw, PAD, y, "PRICE LIST")
    y += 52 + 34
    title_f = font(SERIF, 76)
    for line in wrap(draw, data["title"], title_f, W - 2 * PAD):
        if not dry:
            draw.text((PAD, y), line, font=title_f, fill=CHOCOLATE)
        y += 82
    sub_f = font(SANS, 28)
    for line in wrap(draw, data["subtitle"], sub_f, W - 2 * PAD):
        if not dry:
            draw.text((PAD, y + 8), line, font=sub_f, fill=TAUPE)
        y += 40
    y += 40

    name_f, note_f, group_f = font(SANS_BOLD, 32), font(SANS, 24), font(SANS_BOLD, 22)
    price_w = 270
    for row in data["rows"]:
        if row[0] == "group":
            if not dry:
                draw.text((PAD + 6, y + 20), row[1].upper(), font=group_f, fill=TAUPE)
            y += 62
            continue
        name, note, value, accent = row
        text_w = W - 2 * PAD - 64 - price_w
        note_lines = wrap(draw, note, note_f, text_w)
        h = 44 + 40 + 34 * len(note_lines) + 10
        if not dry:
            draw.rounded_rectangle([PAD, y, W - PAD, y + h], radius=30, fill=ROSE if accent else IVORY)
            draw.text((PAD + 32, y + 30), name, font=name_f, fill=CHOCOLATE)
            for i, line in enumerate(note_lines):
                draw.text((PAD + 32, y + 76 + 34 * i), line, font=note_f,
                          fill=CHOCOLATE if accent else TAUPE)
            price_text(draw, W - PAD - 32, y + h / 2, value)
        y += h + 18

    if data.get("note"):
        y += 14
        for line in wrap(draw, data["note"], note_f, W - 2 * PAD):
            if not dry:
                draw.text((PAD, y), line, font=note_f, fill=TAUPE)
            y += 34

    if data.get("promo"):
        y += 30
        h = 120
        if not dry:
            draw.rounded_rectangle([PAD, y, W - PAD, y + h], radius=30, outline=ROSE, width=3)
            draw.text((PAD + 32, y + 36), "ПРОМОКОД НА ПЕРВЫЙ МЕСЯЦ", font=font(SANS_MED, 22), fill=TAUPE)
            draw.text((PAD + 32, y + 66), config.PROMO_TEXT, font=font(SANS, 24), fill=CHOCOLATE)
            draw.text((W - PAD - 32, y + h / 2 + 4), config.PROMO_CODE, font=font(BEBAS, 60),
                      fill=CHOCOLATE, anchor="rm")
        y += h

    y += 60
    if not dry:
        draw.text((PAD, y), "@RAMAZANOVA_ENG", font=font(BEBAS, 30), fill=TAUPE)
        draw.ellipse([W - PAD - 18, y + 4, W - PAD, y + 22], fill=SAGE)
    return y + 30 + PAD


@lru_cache(maxsize=None)
def price_png(key: str) -> bytes:
    data = dict(PRICES[key], promo=key in PROMO_ON_PRICES)
    probe = ImageDraw.Draw(Image.new("RGB", (W, 10)))
    height = layout(probe, data, dry=True)
    img = Image.new("RGB", (W, int(height)), CREAM)
    layout(ImageDraw.Draw(img), data)
    buf = BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()
