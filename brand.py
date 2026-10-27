# Фирменный стиль @ramazanova_eng: журнальная система для PDF и картинок с ценами.
# Кремовый — основа, бордовый — главный акцент и контрастные поверхности, чёрный — текст.
from pathlib import Path

CREAM = "#F5F0E6"      # светлый фон, бумажные карточки
PAPER = "#FBF8F1"      # лист бумаги поверх кремового фона
BURGUNDY = "#710D19"   # крупные поверхности, акценты
BLACK = "#171615"      # основной текст
WARM_GRAY = "#A7A29E"  # второстепенные подписи, тонкие линии
ESPRESSO = "#3E2723"   # мягкий тёмный для пояснений
PETAL = "#F4C9D6"      # очень дозированно: стикеры, выделенные слова
BEIGE = "#D8C8B8"      # переходы, скотч, разделители

FONTS = Path(__file__).with_name("fonts")
DISPLAY = "PlayfairDisplay_500Medium.ttf"          # крупные заголовки
DISPLAY_BOLD = "PlayfairDisplay_600SemiBold.ttf"   # уровень, цены
ITALIC = "PlayfairDisplay_400Regular_Italic.ttf"   # отдельные слова и подписи
ITALIC_MED = "PlayfairDisplay_500Medium_Italic.ttf"
SANS = "Manrope_400Regular.ttf"                    # основной текст
SANS_MED = "Manrope_500Medium.ttf"
SANS_SEMI = "Manrope_600SemiBold.ttf"
SANS_BOLD = "Manrope_700Bold.ttf"
NARROW = "Oswald_500Medium.ttf"                    # короткие технические подписи

HANDLE = "@RAMAZANOVA_ENG"
