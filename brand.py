# Фирменный стиль @ramazanova_eng: цвета и шрифты для PDF и картинок с ценами.
from pathlib import Path

ESPRESSO = "#3E2723"   # тёмный фон, заголовки и текст
PEONY = "#F4C9D6"      # пилюли-рубрики, акцентные плашки
IVORY = "#F5F0E6"      # фон страницы
PAPER = "#FFFCF7"      # карточки на светлом фоне
WINE = "#7B1E2B"       # акцент: маркеры, рукописные подписи
MUTED = "#8C7B75"      # подписи, второстепенный текст

FONTS = Path(__file__).with_name("fonts")
SANS = "Montserrat_400Regular.ttf"
SANS_MED = "Montserrat_500Medium.ttf"
SANS_SEMI = "Montserrat_600SemiBold.ttf"
SANS_BOLD = "Montserrat_700Bold.ttf"
SERIF = "PlayfairDisplay_600SemiBold.ttf"
SERIF_ITALIC = "PlayfairDisplay_500Medium_Italic.ttf"
SERIF_ITALIC_SEMI = "PlayfairDisplay_600SemiBold_Italic.ttf"
HAND = "Caveat_600SemiBold.ttf"
