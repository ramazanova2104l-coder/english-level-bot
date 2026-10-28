# Тесты под разные цели ученика. В каждом файле: GRAMMAR, TASKS и RECS.
from . import c1, ege, general, kids, oge, travel, work

TRACKS = {
    "general": general,
    "oge": oge,
    "ege": ege,
    "travel": travel,
    "work": work,
    "kids": kids,
}

# Бонусный блок C1 одинаковый для всех целей
for _module in TRACKS.values():
    _module.TASKS.update(c1.TASKS)
