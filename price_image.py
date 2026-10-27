# Рисует картинки с ценами в фирменном стиле @ramazanova_eng из данных formats.PRICES
from functools import lru_cache
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

import brand
import config
from formats import PRICES, PROMO_ON_PRICES

W = 1080
PAD = 72


def font(name: str, size: int):
    return ImageFont.truetype(str(brand.FONTS / name), size)


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


def spaced_width(draw, text, fnt, spacing):
    return sum(draw.textlength(ch, font=fnt) for ch in text) + spacing * (len(text) - 1)


def spaced(draw, x, y, text, fnt, fill, spacing=4, anchor="l"):
    """Подпись узким шрифтом в разрядку (у PIL нет межбуквенного интервала)."""
    if anchor == "r":
        x -= spaced_width(draw, text, fnt, spacing)
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="lm")
        x += draw.textlength(ch, font=fnt) + spacing


def paper(size, color=brand.CREAM, grain=0.05):
    """Фон с деликатным зерном бумаги."""
    noise = Image.merge("RGB", [Image.effect_noise(size, 40)] * 3)
    return Image.blend(Image.new("RGB", size, color), noise, grain).convert("RGBA")


def tape(img, cx, cy, w=150, h=40, angle=-6, color=brand.BEIGE, alpha=200):
    """Кусочек бумажного скотча."""
    piece = Image.new("RGBA", (w, h), color)
    piece.putalpha(alpha)
    piece = piece.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(piece, (int(cx - piece.width / 2), int(cy - piece.height / 2)))


def price_text(draw, right, cy, value, color=brand.BLACK):
    """Цена: цифры Oswald, значок рубля Manrope."""
    if value == "0":
        draw.text((right, cy), "бесплатно", font=font(brand.ITALIC, 44), fill=color, anchor="rm")
        return
    num, rub = font(brand.NARROW, 58), font(brand.SANS_SEMI, 34)
    rub_w = draw.textlength("₽", font=rub)
    draw.text((right, cy + 2), "₽", font=rub, fill=color, anchor="rm")
    draw.text((right - rub_w - 10, cy), value, font=num, fill=color, anchor="rm")


def promo_ticket(width):
    """Промокод на кремовом «билете», который потом слегка повернём и приклеим скотчем."""
    h = 150
    ticket = Image.new("RGBA", (width, h), brand.PAPER)
    d = ImageDraw.Draw(ticket)
    d.rectangle([0, 0, width - 1, h - 1], outline=brand.BEIGE, width=2)
    spaced(d, 36, 48, "ПРОМОКОД НА ПЕРВЫЙ МЕСЯЦ", font(brand.NARROW, 22), brand.WARM_GRAY, spacing=3)
    d.text((36, 96), config.PROMO_TEXT, font=font(brand.SANS, 25), fill=brand.ESPRESSO, anchor="lm")
    d.text((width - 36, h / 2), config.PROMO_CODE, font=font(brand.NARROW, 60), fill=brand.BURGUNDY, anchor="rm")
    return ticket


def layout(img, data, dry=False):
    """Рисует (или только меряет при dry=True) и возвращает итоговую высоту."""
    draw = ImageDraw.Draw(img)
    title_f, sub_f = font(brand.DISPLAY, 74), font(brand.SANS, 28)
    title_lines = wrap(draw, data["title"], title_f, W - 2 * PAD)
    sub_lines = wrap(draw, data["subtitle"], sub_f, W - 2 * PAD)

    # Бордовая шапка
    head_h = PAD + 40 + 40 + 86 * len(title_lines) + 40 * len(sub_lines) + 72
    if not dry:
        draw.rectangle([0, 0, W, head_h], fill=brand.BURGUNDY)
        cap = font(brand.NARROW, 24)
        spaced(draw, PAD, PAD + 10, "PRICE LIST", cap, brand.CREAM)
        spaced(draw, W - PAD, PAD + 10, "ENGLISH LESSONS", cap, brand.CREAM, anchor="r")
        draw.line([PAD, PAD + 40, W - PAD, PAD + 40], fill=brand.CREAM, width=1)
    y = PAD + 40 + 40
    for line in title_lines:
        if not dry:
            draw.text((PAD, y), line, font=title_f, fill=brand.CREAM)
        y += 86
    for line in sub_lines:
        if not dry:
            draw.text((PAD, y + 18), line, font=sub_f, fill=brand.BEIGE)
        y += 40
    y = head_h + 56

    name_f, note_f, group_f = font(brand.SANS_SEMI, 32), font(brand.SANS, 24), font(brand.NARROW, 24)
    price_w = 270
    for row in data["rows"]:
        if row[0] == "group":
            if not dry:
                spaced(draw, PAD, y + 22, row[1].upper(), group_f, brand.BURGUNDY, spacing=3)
            y += 56
            continue
        name, note, value, accent = row
        text_w = W - 2 * PAD - 64 - price_w
        note_lines = wrap(draw, note, note_f, text_w)
        h = 44 + 40 + 34 * len(note_lines) + 10
        if not dry:
            if accent:  # выгодный вариант: бордовая карточка, сверху розовый скотч
                draw.rectangle([PAD, y, W - PAD, y + h], fill=brand.BURGUNDY)
                tape(img, W - PAD - 70, y + 2, w=120, h=34, angle=7, color=brand.PETAL, alpha=230)
            else:
                draw.line([PAD, y, W - PAD, y], fill=brand.BLACK, width=2)
            ink, sub = (brand.CREAM, brand.BEIGE) if accent else (brand.BLACK, brand.ESPRESSO)
            draw.text((PAD + 32, y + 30), name, font=name_f, fill=ink)
            for i, line in enumerate(note_lines):
                draw.text((PAD + 32, y + 76 + 34 * i), line, font=note_f, fill=sub)
            price_text(draw, W - PAD - 32, y + h / 2, value, ink)
        y += h + 18

    if data.get("note"):
        y += 14
        for line in wrap(draw, data["note"], note_f, W - 2 * PAD):
            if not dry:
                draw.text((PAD, y), line, font=note_f, fill=brand.ESPRESSO)
            y += 34

    if data.get("promo"):
        y += 50
        ticket = promo_ticket(W - 2 * PAD - 20)
        if not dry:
            tilted = ticket.rotate(0.8, expand=True, resample=Image.BICUBIC)
            shadow = Image.new("RGBA", ticket.size, brand.BEIGE).rotate(-1.5, expand=True, resample=Image.BICUBIC)
            img.alpha_composite(shadow, (PAD + 6, y + 8))
            img.alpha_composite(tilted, (PAD + 4, y))
            tape(img, PAD + 150, y + 6)
        y += ticket.height + 20

    y += 60
    if not dry:
        draw.line([PAD, y, W - PAD, y], fill=brand.WARM_GRAY, width=1)
        spaced(draw, PAD, y + 40, brand.HANDLE, font(brand.NARROW, 24), brand.WARM_GRAY)
        draw.text((W - PAD, y + 40), f"with love, {config.TEACHER_NAME}", font=font(brand.ITALIC, 30),
                  fill=brand.BURGUNDY, anchor="rm")
    return y + 40 + PAD


@lru_cache(maxsize=None)
def price_png(key: str) -> bytes:
    data = dict(PRICES[key], promo=key in PROMO_ON_PRICES)
    height = layout(Image.new("RGBA", (W, 10)), data, dry=True)
    img = paper((W, int(height)))
    layout(img, data)
    buf = BytesIO()
    img.convert("RGB").save(buf, "PNG", optimize=True)
    return buf.getvalue()
