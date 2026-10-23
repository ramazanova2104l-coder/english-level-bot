# Тесты под разные цели ученика. В каждом файле: GRAMMAR, TASKS и RECS.
from . import ege, general, kids, oge, travel, work

TRACKS = {
    "general": general,
    "oge": oge,
    "ege": ege,
    "travel": travel,
    "work": work,
    "kids": kids,
}
