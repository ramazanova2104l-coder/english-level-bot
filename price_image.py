# Рисует картинки с ценами в фирменном стиле @ramazanova_eng из данных formats.PRICES
from functools import lru_cache
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import config
from formats import PRICES, PROMO_ON_PRICES

import brand

FONTS = brand.FONTS
BG = brand.ESPRESSO
CARD = brand.PAPER
ACCENT = brand.PEONY
TEXT = brand.ESPRESSO
LIGHT = brand.IVORY
MUTED = brand.MUTED
SOFT = "#CDBFB8"  # приглушённый светлый текст на тёмном фоне

W = 1080
PAD = 72


def font(name: str, size: int):
    return ImageFont.truetype(str(FONTS / name), size)


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


def spaced(label: str) -> str:
    return " ".join(label.upper())


def pill(draw, x, y, label, fill=ACCENT):
    fnt = font(brand.SANS_BOLD, 22)
    text = spaced(label)
    w = draw.textlength(text, font=fnt) + 56
    draw.rounded_rectangle([x, y, x + w, y + 52], radius=26, fill=fill)
    draw.text((x + 28, y + 27), text, font=fnt, fill=TEXT, anchor="lm")
    return w


def price_text(draw, right, cy, value):
    if value == "0":
        draw.text((right, cy), "бесплатно", font=font(brand.SERIF_ITALIC, 40), fill=TEXT, anchor="rm")
        return
    num, rub = font(brand.SERIF, 58), font(brand.SANS_SEMI, 32)
    rub_w = draw.textlength("₽", font=rub)
    draw.text((right, cy + 2), "₽", font=rub, fill=TEXT, anchor="rm")
    draw.text((right - rub_w - 12, cy), value, font=num, fill=TEXT, anchor="rm")


def layout(draw, data, dry=False):
    """Рисует (или только меряет при dry=True) и возвращает итоговую высоту."""
    y = PAD
    if not dry:
        pill(draw, PAD, y, "price list")
    y += 52 + 36
    title_f = font(brand.SERIF_ITALIC, 76)
    for line in wrap(draw, data["title"], title_f, W - 2 * PAD):
        if not dry:
            draw.text((PAD, y), line, font=title_f, fill=LIGHT)
        y += 90
    sub_f = font(brand.SANS, 27)
    for line in wrap(draw, data["subtitle"], sub_f, W - 2 * PAD):
        if not dry:
            draw.text((PAD, y + 8), line, font=sub_f, fill=SOFT)
        y += 40
    y += 44

    name_f, note_f, group_f = font(brand.SANS_SEMI, 31), font(brand.SANS, 24), font(brand.SANS_BOLD, 20)
    price_w = 280
    for row in data["rows"]:
        if row[0] == "group":
            if not dry:
                draw.text((PAD + 6, y + 22), spaced(row[1]), font=group_f, fill=ACCENT)
            y += 64
            continue
        name, note, value, accent = row
        text_w = W - 2 * PAD - 64 - price_w
        note_lines = wrap(draw, note, note_f, text_w)
        h = 44 + 40 + 34 * len(note_lines) + 10
        if not dry:
            draw.rounded_rectangle([PAD, y, W - PAD, y + h], radius=30, fill=ACCENT if accent else CARD)
            draw.text((PAD + 32, y + 30), name, font=name_f, fill=TEXT)
            for i, line in enumerate(note_lines):
                draw.text((PAD + 32, y + 76 + 34 * i), line, font=note_f, fill=TEXT if accent else MUTED)
            price_text(draw, W - PAD - 32, y + h / 2, value)
        y += h + 18

    if data.get("note"):
        y += 14
        for line in wrap(draw, data["note"], note_f, W - 2 * PAD):
            if not dry:
                draw.text((PAD, y), line, font=note_f, fill=SOFT)
            y += 34

    if data.get("promo"):
        y += 30
        h = 124
        if not dry:
            draw.rounded_rectangle([PAD, y, W - PAD, y + h], radius=30, outline=ACCENT, width=3)
            draw.text((PAD + 32, y + 34), spaced("промокод на первый месяц"), font=font(brand.SANS_BOLD, 18),
                      fill=ACCENT)
            draw.text((PAD + 32, y + 70), config.PROMO_TEXT, font=font(brand.SANS, 24), fill=LIGHT)
            draw.text((W - PAD - 32, y + h / 2), config.PROMO_CODE, font=font(brand.SERIF, 52),
                      fill=ACCENT, anchor="rm")
        y += h

    y += 56
    if not dry:
        draw.text((PAD, y + 14), spaced("@ramazanova_eng"), font=font(brand.SANS_SEMI, 20), fill=SOFT)
        draw.text((W - PAD, y + 10), f"with love, {config.TEACHER_NAME}", font=font(brand.HAND, 44),
                  fill=ACCENT, anchor="rm")
    return y + 40 + PAD


@lru_cache(maxsize=None)
def price_png(key: str) -> bytes:
    data = dict(PRICES[key], promo=key in PROMO_ON_PRICES)
    probe = ImageDraw.Draw(Image.new("RGB", (W, 10)))
    height = layout(probe, data, dry=True)
    img = Image.new("RGB", (W, int(height)), BG)
    layout(ImageDraw.Draw(img), data)
    buf = BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()
