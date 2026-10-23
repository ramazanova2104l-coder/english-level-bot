# Тест «ЕГЭ»: задания в формате экзамена за 11 класс
# (грамматика и словообразование, True / False / Not stated, заголовки к абзацам, вопросы к интервью и статье).
# Первый вариант ответа в каждом вопросе - правильный, бот перемешивает варианты сам.
# Вопросы с "fixed": True показываются в заданном порядке, правильный ответ - "answer".

from .oge import GRAMMAR as OGE_GRAMMAR

TFN = ["True", "False", "Not stated"]
HEADINGS = [
    "Learning the value of money",
    "A risk for school results",
    "A short taste of working life",
    "Becoming more confident",
    "Finding a job online",
]

# ---- Часть 1. Грамматика и лексика ----
# A1 и A2 общие с ОГЭ, B1-C1 свои, в формате заданий 19-36 ЕГЭ.
GRAMMAR = {
    "A1": OGE_GRAMMAR["A1"],
    "A2": OGE_GRAMMAR["A2"],
    "B1": [
        {"text": "The first Olympic Games ___ in Greece. (HOLD)",
         "options": ["were held", "held", "have held", "was held"]},
        {"text": "If I were you, I ___ this offer. (ACCEPT)",
         "options": ["would accept", "will accept", "accepted", "would have accepted"]},
        {"text": "My grandmother has never ___ abroad. (TRAVEL)",
         "options": ["travelled", "travel", "travels", "travelling"]},
        {"text": "It was the ___ day of my life! (HAPPY)",
         "options": ["happiest", "happier", "most happy", "happyest"]},
        {"text": "He felt ___ because nobody listened to him. (HAPPY)",
         "options": ["unhappy", "happiness", "happily", "unhappily"]},
    ],
    "B2": [
        {"text": "The teacher asked us what we ___ during the holidays. (DO)",
         "options": ["had done", "will do", "have done", "do"]},
        {"text": "Nobody expected such a ___ result. (DISAPPOINT)",
         "options": ["disappointing", "disappointed", "disappointment", "disappoint"]},
        {"text": "The ___ of the village were very friendly. (INHABIT)",
         "options": ["inhabitants", "inhabitation", "inhabited", "inhabits"]},
        {"text": "His story was so ___ that nobody believed it. (BELIEVE)",
         "options": ["unbelievable", "believable", "unbelieving", "disbelief"]},
        {"text": "By 2035, scientists ___ a cure for this disease. (FIND)",
         "options": ["will have found", "will find", "find", "have found"]},
    ],
    "C1": [
        {"text": "Under no circumstances ___ use your phone during the exam.",
         "options": ["should you", "you should", "you can", "can't you"]},
        {"text": "His argument doesn't ___ water: there's no evidence for it.",
         "options": ["hold", "keep", "carry", "take"]},
        {"text": "They had to ___ the trip until the weather improved.",
         "options": ["put off", "take off", "set off", "call off"]},
        {"text": "She ___ a great impression on the examiners.",
         "options": ["made", "did", "gave", "took"]},
        {"text": "It's high time you ___ seriously about your future.",
         "options": ["started thinking", "start thinking", "to start thinking", "have started thinking"]},
    ],
}

# ---- Части 2 и 3. Аудирование и чтение ----
TASKS = {
    "listen_easy": {
        "kind": "listening",
        # Диалог: каждая строка начинается с имени, у каждого свой голос
        "voices": {"Tom": "am_michael", "Kate": "af_heart"}, "speed": 0.95,
        "intro": "🎧 <b>Аудирование, задание 1</b> (формат ЕГЭ, задание 2)\n\nПослушай диалог. "
                 "Для каждого утверждения выбери: <b>True</b> (верно), <b>False</b> (неверно) "
                 "или <b>Not stated</b> (в разговоре не сказано).",
        "script": (
            "Tom: Hi Kate! I heard you've decided to take a gap year before university. Is that true?\n"
            "Kate: Yes, it is. My parents weren't very keen on the idea at first, but I managed to convince them.\n"
            "Tom: So what are you planning to do?\n"
            "Kate: I'm going to spend six months volunteering at a wildlife centre in Costa Rica. I'll be looking "
            "after injured animals, mostly birds and monkeys.\n"
            "Tom: Wow, that sounds amazing. Isn't it expensive, though?\n"
            "Kate: The flights are, but the centre provides food and accommodation for volunteers, so it's not as "
            "bad as you'd think. I've been working at a café since September to save up.\n"
            "Tom: And what about after that?\n"
            "Kate: I'll come back in the spring and start studying biology in September. I think the experience "
            "will help me decide which area of biology I want to focus on."
        ),
        "questions": [
            {"text": "Kate's parents supported her plan from the very beginning.",
             "options": TFN, "fixed": True, "answer": 1},
            {"text": "Kate is going to work with animals in Costa Rica.", "options": TFN, "fixed": True, "answer": 0},
            {"text": "Volunteers have to pay for their accommodation.", "options": TFN, "fixed": True, "answer": 1},
            {"text": "Kate has been to Costa Rica before.", "options": TFN, "fixed": True, "answer": 2},
        ],
    },
    "listen_hard": {
        "kind": "listening",
        "voices": {"Interviewer": "af_bella", "Daniel": "am_adam"}, "speed": 1.0,
        "intro": "🎧 <b>Аудирование, задание 2</b> (формат ЕГЭ, задания 3-9)\n\nИнтервью с переводчиком. "
                 "Выбери правильный ответ на каждый из 4 вопросов.",
        "script": (
            "Interviewer: Today I'm talking to Daniel Hart, a professional translator who works with eight languages. "
            "Daniel, was it always your plan to become a translator?\n"
            "Daniel: Not at all. At school I was actually much better at maths, and everyone assumed I'd become an "
            "engineer. Languages were something I did for fun, mainly because I wanted to understand the songs I was "
            "listening to. It was only when I spent a year in Spain as a student that I realised I could make a "
            "living from it.\n"
            "Interviewer: Many people believe that machine translation will soon make your job unnecessary. "
            "Do you worry about that?\n"
            "Daniel: I'd be lying if I said it never crossed my mind. But in my experience, machines are very good "
            "at translating the words and surprisingly bad at translating the meaning. A joke, a bit of irony, a "
            "phrase that sounds polite in one culture and rude in another: that's still where a human makes the "
            "difference. What has changed is that I now spend less time translating from scratch and more time "
            "editing and checking.\n"
            "Interviewer: What advice would you give to young people who want to work with languages?\n"
            "Daniel: Don't just study the language, study the people who speak it. Read their newspapers, watch "
            "their comedies, find out what makes them laugh and what makes them angry. Grammar can be learned from "
            "a book. That kind of understanding can't."
        ),
        "questions": [
            {"text": "Why did Daniel first become interested in languages?",
             "options": ["He wanted to understand the songs he listened to", "His teachers advised him to",
                         "He was bad at maths", "He had always planned to be a translator"]},
            {"text": "What is Daniel's attitude to machine translation?",
             "options": ["It has worried him, but he thinks humans are still needed",
                         "He is sure it will soon replace translators",
                         "He refuses to use it", "He thinks it translates meaning better than words"]},
            {"text": "How has Daniel's work changed?",
             "options": ["He edits and checks more than he translates from scratch",
                         "He translates more jokes than before", "He works with fewer languages",
                         "He has stopped translating"]},
            {"text": "What is Daniel's main advice to young people?",
             "options": ["Learn about the culture, not only the language", "Study grammar from books",
                         "Learn as many languages as possible", "Avoid machine translation"]},
        ],
    },
    "read_easy": {
        "kind": "reading",
        "intro": "📖 <b>Чтение, задание 1</b> (формат ЕГЭ, задание 10)\n\nПрочитай текст и подбери "
                 "к каждому абзацу (A-D) подходящий заголовок. Один заголовок лишний.",
        "text": (
            "<b>Teenagers and Part-time Jobs</b>\n\n"
            "<b>A.</b> Many teenagers dream of having their own money, and a part-time job seems the obvious "
            "solution. Working in a café or delivering newspapers not only brings in some cash but also shows young "
            "people how hard it can be to earn it.\n\n"
            "<b>B.</b> However, experts warn that too much work can harm school results. Students who work more than "
            "fifteen hours a week often feel tired in class and have less time for homework and revision.\n\n"
            "<b>C.</b> Some schools have found a creative way to give students work experience without the long "
            "hours. They organise one-week placements in local companies, where teenagers can see what a real "
            "working day looks like.\n\n"
            "<b>D.</b> For many young people, the biggest benefit of a job is not the money at all. They say that "
            "dealing with customers and colleagues has made them more confident and better at solving problems."
        ),
        "questions": [
            {"text": "Which heading fits paragraph A?", "options": HEADINGS, "fixed": True, "answer": 0},
            {"text": "Which heading fits paragraph B?", "options": HEADINGS, "fixed": True, "answer": 1},
            {"text": "Which heading fits paragraph C?", "options": HEADINGS, "fixed": True, "answer": 2},
            {"text": "Which heading fits paragraph D?", "options": HEADINGS, "fixed": True, "answer": 3},
        ],
    },
    "read_hard": {
        "kind": "reading",
        "intro": "📖 <b>Чтение, задание 2</b> (формат ЕГЭ, задания 12-18)\n\nПрочитай статью "
                 "и выбери правильный ответ на каждый из 4 вопросов.",
        "text": (
            "<b>In Praise of Boredom</b>\n\n"
            "For most of us, boredom is something to be avoided at all costs. The moment we find ourselves waiting "
            "in a queue or sitting on a train, we reach for our phones. Yet a number of psychologists now argue that "
            "this constant escape from boredom may come at a price. In one frequently cited experiment, participants "
            "who had first been given a deliberately dull task, copying numbers from a telephone directory, went on "
            "to produce noticeably more creative ideas than those who had not. The researchers suggest that when the "
            "mind is left unoccupied, it begins to wander, and it is precisely in this wandering that unexpected "
            "connections are made.\n\n"
            "This is not to say that boredom is always beneficial. Chronic boredom, the kind experienced by people "
            "stuck in unfulfilling jobs, has been linked to stress and even depression. The point, rather, is that "
            "short periods of having nothing to do are not a problem to be solved, but an opportunity that we have "
            "largely forgotten how to use."
        ),
        "questions": [
            {"text": "What did the experiment show?",
             "options": ["A boring task was followed by more creative thinking",
                         "Boring tasks make people stressed", "Most people refuse to do dull tasks",
                         "Creative people get bored more easily"]},
            {"text": "According to the researchers, why might boredom lead to creativity?",
             "options": ["A wandering mind makes unexpected connections", "Bored people try harder",
                         "Boredom reduces stress", "People want to impress the researchers"]},
            {"text": "The word \"chronic\" in the text is closest in meaning to...",
             "options": ["long-lasting", "sudden", "mild", "rare"]},
            {"text": "What is the writer's main point in the last paragraph?",
             "options": ["Short periods of boredom can be valuable", "Boredom is always harmful",
                         "People should leave boring jobs", "Phones are the main cause of depression"]},
        ],
    },
}

# ---- Блок в PDF ----
TARGETS = {"ЕГЭ": ("B2", "на 80+ баллов обычно нужен уровень B1+-B2")}

RECS = {
    "title": "Твоя цель: сдать ЕГЭ",
    "tips": [
        "Начни с демоверсии ФИПИ: в ней точный формат всех заданий и критерии оценки письменной и устной части.",
        "Раз в 2-3 недели решай полный вариант на время, остальное время закрывай слабые места.",
        "Грамматика и словообразование (задания 19-29) дают быстрые баллы: учи правила и суффиксы блоками.",
        "Эссе и устная часть оцениваются по структуре не меньше, чем по содержанию: учи план ответа и пиши с проверкой.",
        "Читай и слушай английский не только по сборникам: сериалы, подкасты и статьи расширяют словарь быстрее.",
    ],
    "resources": [
        "Демоверсии и открытый банк заданий на сайте ФИПИ (fipi.ru).",
        "Сборники М. В. Вербицкой для подготовки к ЕГЭ.",
        "Macmillan «Exam Skills for Russia»: отдельные книги по грамматике, чтению и письму.",
    ],
}
