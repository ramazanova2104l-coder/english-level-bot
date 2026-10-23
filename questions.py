import math

# Вопросы теста. Первый вариант ответа в каждом вопросе — правильный
# (бот сам перемешивает варианты перед показом).
# По 4 вопроса на каждый уровень, от простого к сложному.

QUESTIONS = [
    # --- A1 ---
    {"level": "A1", "text": "She ___ a teacher.", "options": ["is", "am", "are", "be"]},
    {"level": "A1", "text": "I ___ like coffee.", "options": ["don't", "doesn't", "not", "no"]},
    {"level": "A1", "text": "There ___ two cats in the room.", "options": ["are", "is", "am", "be"]},
    {"level": "A1", "text": "___ you speak English?", "options": ["Do", "Does", "Are", "Is"]},
    # --- A2 ---
    {"level": "A2", "text": "Yesterday I ___ to the cinema.", "options": ["went", "go", "gone", "goes"]},
    {"level": "A2", "text": "This book is ___ than that one.",
     "options": ["more interesting", "interestinger", "most interesting", "the more interesting"]},
    {"level": "A2", "text": "I ___ TV when you called.",
     "options": ["was watching", "watched", "am watching", "watch"]},
    {"level": "A2", "text": "How ___ money do you have?", "options": ["much", "many", "lot", "few"]},
    # --- B1 ---
    {"level": "B1", "text": "I ___ in Moscow since 2015.",
     "options": ["have lived", "live", "am living", "lived"]},
    {"level": "B1", "text": "If it rains tomorrow, we ___ at home.",
     "options": ["will stay", "stay", "would stay", "stayed"]},
    {"level": "B1", "text": "The letter ___ yesterday.",
     "options": ["was sent", "sent", "has sent", "is sent"]},
    {"level": "B1", "text": "He suggested ___ a taxi.",
     "options": ["taking", "to take", "take", "took"]},
    # --- B2 ---
    {"level": "B2", "text": "If I ___ about the meeting, I would have come.",
     "options": ["had known", "knew", "have known", "would know"]},
    {"level": "B2", "text": "By the time we arrived, the film ___.",
     "options": ["had already started", "already started", "has already started", "was already starting"]},
    {"level": "B2", "text": "I wish I ___ more time to study.",
     "options": ["had", "have", "would have", "having"]},
    {"level": "B2", "text": "You ___ have told me! I would have helped.",
     "options": ["should", "must", "can", "would"]},
    # --- C1 ---
    {"level": "C1", "text": "Hardly ___ the house when it started to rain.",
     "options": ["had I left", "I had left", "I left", "did I leave"]},
    {"level": "C1", "text": "It's high time we ___ a decision.",
     "options": ["made", "make", "will make", "have made"]},
    {"level": "C1", "text": "Not only ___ late, but he also forgot the tickets.",
     "options": ["was he", "he was", "he is", "did he"]},
    {"level": "C1", "text": "The new law will ___ affect small businesses.",
     "options": ["adversely", "adverse", "averse", "aversely"]},
]

LEVELS = ["A1", "A2", "B1", "B2", "C1"]

# Описание результата для ученика
RESULTS = {
    "A0": ("Starter (A0–A1)",
           "Вы только начинаете путь в английском, и это отличный момент, чтобы сразу "
           "поставить правильную базу: произношение, простые фразы и основные времена."),
    "A1": ("Beginner (A1)",
           "Вы знаете самые основы: to be, простые вопросы и отрицания. Следующий шаг — "
           "прошедшее время и уверенные фразы для повседневных ситуаций."),
    "A2": ("Elementary (A2)",
           "Вы можете рассказать о себе и справиться с простыми ситуациями. Дальше — "
           "Present Perfect, условные предложения и больше живой речи, чтобы перестать "
           "переводить в голове."),
    "B1": ("Intermediate (B1)",
           "Хороший уровень: вы понимаете основное и можете общаться на знакомые темы. "
           "Чтобы выйти на B2, нужны сложные времена, богатая лексика и много разговорной практики."),
    "B2": ("Upper-Intermediate (B2)",
           "Сильный уровень! Вы свободно общаетесь на большинство тем. Дальше — "
           "продвинутые конструкции, идиомы и беглость речи без пауз."),
    "C1": ("Advanced (C1)",
           "Впечатляет! Вы владеете продвинутой грамматикой. Чтобы держать уровень, "
           "важна регулярная разговорная практика и точная, естественная лексика."),
}


def calc_level(correct_by_level: dict, asked_by_level: dict) -> str:
    """Уровень = самый высокий, на котором (и на всех ниже) верно минимум 60% вопросов.
    На A1 это 3 из 4, на A2–C1 (грамматика + аудио + текст) это 4 из 6."""
    result = "A0"
    for level in LEVELS:
        asked = asked_by_level.get(level, 0)
        if asked and correct_by_level.get(level, 0) >= math.ceil(asked * 0.6):
            result = level
        else:
            break
    return result


# ---- Аудирование ----
# Запись лежит в папке media (файл listening.mp3, .m4a, .ogg или .wav).
# Если файла нет, бот просто пропускает этот блок.
LISTENING = {
    "intro": "🎧 <b>Аудирование</b>\n\nПослушайте короткий рассказ (меньше минуты) и ответьте на 4 вопроса. "
             "Можно слушать несколько раз.",
    # Текст, который нужно начитать для записи
    "script": (
        "Hi, my name is Kate. I'm a nurse, and I live in a small town near Boston. "
        "Every morning I get up at six o'clock, because my shift starts at half past seven. "
        "I usually go to work by bike, unless it's raining. Then I take the bus. "
        "Last year I decided to learn Spanish, because I'd always wanted to travel around South America. "
        "At first it was really hard, and I nearly gave up after a couple of months. "
        "But then I found a conversation group that meets online on Thursday evenings, "
        "and that changed everything. Now I'm planning a trip to Peru next spring. "
        "If I hadn't joined that group, I don't think I'd still be learning."
    ),
    "questions": [
        {"level": "A2", "text": "What is Kate's job?",
         "options": ["A nurse", "A teacher", "A doctor", "A student"]},
        {"level": "B1", "text": "How does Kate get to work when it rains?",
         "options": ["By bus", "By bike", "By car", "On foot"]},
        {"level": "B2", "text": "Why did Kate start learning Spanish?",
         "options": ["She had always wanted to travel in South America", "Her job required it",
                     "Her best friend is from Peru", "She was moving to Spain"]},
        {"level": "C1", "text": "What does Kate suggest about the conversation group?",
         "options": ["It is the reason she didn't give up", "It was too expensive for her",
                     "She doesn't go there any more", "It meets every morning"]},
    ],
}

# ---- Чтение ----
READING = {
    "intro": "📖 <b>Чтение</b>\n\nПрочитайте текст и ответьте на 4 вопроса.",
    "text": (
        "<b>The Four-Day Week</b>\n\n"
        "Last year, several companies in the UK took part in an experiment: for six months, "
        "employees worked four days a week instead of five, but received the same salary. "
        "The results surprised many sceptics. Most companies reported that productivity stayed "
        "the same or even improved, while staff said they felt less stressed and slept better. "
        "Interestingly, the number of people taking sick days fell significantly.\n\n"
        "However, the idea does not suit every business. Hospitals and shops, for example, need "
        "people available every day, so they would have to hire more staff. Despite this, over "
        "ninety percent of the companies decided to continue with the four-day week after the "
        "trial ended."
    ),
    "questions": [
        {"level": "A2", "text": "How long did the experiment last?",
         "options": ["Six months", "One year", "Four days", "Five weeks"]},
        {"level": "B1", "text": "What happened to the employees' salaries?",
         "options": ["They stayed the same", "They went down", "They went up",
                     "They were paid for four days only"]},
        {"level": "B2", "text": "Why might a four-day week be difficult for hospitals?",
         "options": ["They need staff every day", "Doctors don't want it",
                     "It is too expensive for patients", "Hospitals didn't take part in the trial"]},
        {"level": "C1", "text": "The word \"sceptics\" refers to people who...",
         "options": ["doubted the idea would work", "organised the experiment",
                     "worked at the companies", "often took sick days"]},
    ],
}
