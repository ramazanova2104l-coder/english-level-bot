# Тесты под разные цели ученика. В каждом файле: GRAMMAR, TASKS и RECS.
from . import exam, general, kids, travel, work

TRACKS = {
    "general": general,
    "exam": exam,
    "travel": travel,
    "work": work,
    "kids": kids,
}
