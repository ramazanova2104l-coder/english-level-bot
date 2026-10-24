# Фирменный стиль @ramazanova_eng: цвета и шрифты для PDF и картинок с ценами.
from pathlib import Path

DARK = "#7A1015"       # бордовый: обложка, блок с промокодом, фон картинок с ценами
INK = "#1F1B19"        # основной текст и заголовки
BG = "#EEE5D7"         # бежевый фон страницы («бумага»)
CARD = "#F8F3EB"       # карточки
ACCENT = "#8E1B1F"     # красный акцент: рубрики, маркеры, рукописные подписи
HIGHLIGHT = "#E2D2BD"  # тёплый бежевый: выделенные карточки
MUTED = "#8A7F78"      # подписи, второстепенный текст
ON_DARK = "#F3EBDD"    # светлый текст на бордовом

FONTS = Path(__file__).with_name("fonts")
SANS = "Montserrat_400Regular.ttf"
SANS_MED = "Montserrat_500Medium.ttf"
SANS_SEMI = "Montserrat_600SemiBold.ttf"
SANS_BOLD = "Montserrat_700Bold.ttf"
TITLE = "Oswald_600SemiBold.ttf"        # узкие заглавные заголовки
TITLE_MED = "Oswald_500Medium.ttf"
HAND = "MarckScript_400Regular.ttf"     # рукописные акценты
