# Тест «ОГЭ / ЕГЭ»: задания в формате школьных экзаменов
# (преобразование слова в скобках, словообразование, True / False / Not stated).
# Первый вариант ответа в каждом вопросе — правильный, бот перемешивает варианты сам.
# Вопросы с "fixed": True показываются в заданном порядке, правильный ответ — "answer".

TFN = ["True", "False", "Not stated"]

# ---- Часть 1. Грамматика и лексика ----
GRAMMAR = {
    "A1": [
        {"text": "My brother ___ in Moscow. (LIVE)", "options": ["lives", "live", "living", "is live"]},
        {"text": "There are three new ___ in our class. (BOY)", "options": ["boys", "boyes", "boy", "boies"]},
        {"text": "We ___ good friends. (BE)", "options": ["are", "is", "am", "be"]},
        {"text": "This is ___ school bag. (I)", "options": ["my", "me", "mine", "I"]},
        {"text": "Kate ___ TV every evening. (WATCH)", "options": ["watches", "watchs", "watch", "watching"]},
    ],
    "A2": [
        {"text": "Yesterday we ___ to the museum. (GO)", "options": ["went", "goed", "have gone", "go"]},
        {"text": "This summer was ___ than last summer. (HOT)", "options": ["hotter", "more hot", "hottest", "hoter"]},
        {"text": "Look! The children ___ football in the yard. (PLAY)",
         "options": ["are playing", "play", "plays", "played"]},
        {"text": "She is a famous ___. (SING)", "options": ["singer", "singing", "song", "singed"]},
        {"text": "I ___ my homework yet. (NOT FINISH)",
         "options": ["haven't finished", "didn't finish", "don't finish", "not finished"]},
    ],
    "B1": [
        {"text": "The letter ___ two days ago. (SEND)",
         "options": ["was sent", "sent", "has been sent", "is sent"]},
        {"text": "If it ___ tomorrow, we will stay at home. (RAIN)",
         "options": ["rains", "will rain", "rained", "would rain"]},
        {"text": "Mary said that she ___ tired. (BE)", "options": ["was", "be", "were", "being"]},
        {"text": "It was a warm and ___ day. (SUN)", "options": ["sunny", "sunful", "sunned", "sunning"]},
        {"text": "The film was so ___ that we left early. (BORE)",
         "options": ["boring", "bored", "boredom", "bore"]},
    ],
    "B2": [
        {"text": "By the time we arrived, the concert ___. (ALREADY START)",
         "options": ["had already started", "already started", "has already started", "was already starting"]},
        {"text": "Smoking is ___ to your health. (HARM)", "options": ["harmful", "harmless", "harming", "harmed"]},
        {"text": "He was ___ about his chances of winning. (OPTIMISM)",
         "options": ["optimistic", "optimism", "optimist", "optimistically"]},
        {"text": "The museum, ___ was built in 1850, attracts many tourists.",
         "options": ["which", "that", "what", "who"]},
        {"text": "The ___ of the new bridge took three years. (CONSTRUCT)",
         "options": ["construction", "constructor", "constructive", "constructing"]},
    ],
    "C1": [
        {"text": "He ___ his success to hard work and a bit of luck.",
         "options": ["attributed", "explained", "referred", "blamed"]},
        {"text": "Hardly had the lesson begun ___ the fire alarm went off.",
         "options": ["when", "than", "then", "that"]},
        {"text": "The ___ of the town has doubled in ten years. (POPULATE)",
         "options": ["population", "popularity", "populous", "populated"]},
        {"text": "Although everyone knew she was wrong, she was ___ to admit it. (WILLING)",
         "options": ["unwilling", "willingly", "unwillingly", "willingness"]},
        {"text": "It was such a ___ performance that the audience stood up and cheered. (REMARK)",
         "options": ["remarkable", "remarked", "remarking", "remarkably"]},
    ],
}

# ---- Части 2 и 3. Аудирование и чтение ----
TASKS = {
    "listen_easy": {
        "kind": "listening",
        "voice": "af_bella", "speed": 0.88,
        "intro": "🎧 <b>Аудирование, задание 1</b> (формат ОГЭ)\n\nПослушайте школьное объявление "
                 "и ответьте на 4 вопроса. Можно слушать несколько раз.",
        "script": (
            "Good morning, everyone. This is an announcement for all students in years eight and nine. "
            "This Friday there will be no lessons after lunch, because the school is holding its annual sports day. "
            "Please bring your sports clothes and a bottle of water. "
            "The competitions will start at one o'clock at the main stadium. "
            "If it rains, they will take place in the gym instead. "
            "Students who want to take part in the running races should give their names to Mr Ivanov before Wednesday. "
            "Parents are welcome to come and watch. Thank you."
        ),
        "questions": [
            {"text": "Who is the announcement for?",
             "options": ["Students in years 8 and 9", "All parents", "Teachers only", "Students in year 11"]},
            {"text": "Why will there be no lessons on Friday afternoon?",
             "options": ["Because of sports day", "Because of a school trip", "Because of exams",
                         "Because teachers have a meeting"]},
            {"text": "Where will the competitions be if it rains?",
             "options": ["In the gym", "At the main stadium", "In the classrooms", "They will be cancelled"]},
            {"text": "What should students do before Wednesday if they want to run in the races?",
             "options": ["Give their names to Mr Ivanov", "Buy new sports clothes",
                         "Bring their parents", "Pay for a ticket"]},
        ],
    },
    "listen_hard": {
        "kind": "listening",
        # Диалог: строки, которые начинаются с "Interviewer:" и "Anna:", озвучиваются разными голосами
        "voices": {"Interviewer": "am_michael", "Anna": "af_heart"}, "speed": 1.0,
        "intro": "🎧 <b>Аудирование, задание 2</b> (формат ЕГЭ)\n\nИнтервью с выпускницей. "
                 "Ответьте на 4 вопроса.",
        "script": (
            "Interviewer: So, Anna, you got one of the highest scores in the country in English. What was your secret?\n"
            "Anna: Honestly, there wasn't really a secret. I'd say the most important thing was that I started "
            "preparing early, in tenth grade, rather than leaving it until the last few months. And I didn't just "
            "do practice tests. I actually think a lot of students overdo those. I read books and watched series in "
            "English because I enjoyed it, and that helped my vocabulary far more than memorising word lists.\n"
            "Interviewer: Was there any part of the exam you found particularly difficult?\n"
            "Anna: The essay, definitely. At first my essays were full of ideas but badly organised. My teacher kept "
            "telling me that examiners care about structure just as much as content, and once I started planning "
            "each paragraph before writing, my marks went up quite quickly."
        ),
        "questions": [
            {"text": "When did Anna start preparing for the exam?",
             "options": ["In tenth grade", "In the last few months", "In primary school",
                         "After her first practice test"]},
            {"text": "What does Anna think about practice tests?",
             "options": ["Many students do too many of them", "They are the best way to prepare",
                         "They are completely useless", "She never did any"]},
            {"text": "What helped Anna's vocabulary most?",
             "options": ["Reading and watching series she enjoyed", "Memorising word lists",
                         "Doing practice tests", "Talking to examiners"]},
            {"text": "What improved Anna's essay marks?",
             "options": ["Planning each paragraph before writing", "Adding more ideas",
                         "Writing longer essays", "Learning model essays by heart"]},
        ],
    },
    "read_easy": {
        "kind": "reading",
        "intro": "📖 <b>Чтение, задание 1</b> (формат ОГЭ)\n\nПрочитайте текст. Для каждого утверждения выберите: "
                 "<b>True</b> (верно), <b>False</b> (неверно) или <b>Not stated</b> (в тексте не сказано).",
        "text": (
            "<b>Our School Trip</b>\n\n"
            "Last month our class went on a trip to Kazan. We travelled by train, and the journey took about twelve "
            "hours. Most of us had never been to Kazan before, so we were very excited. On the first day we visited "
            "the Kremlin and took a lot of photos. In the evening our teacher, Mrs Petrova, took us to a café where "
            "we tried traditional Tatar food. On the second day it was raining, so instead of walking around the "
            "city we went to a science museum. Everyone agreed it was the best part of the trip. We came home tired "
            "but happy, and now we are planning our next trip."
        ),
        "questions": [
            {"text": "The class travelled to Kazan by plane.", "options": TFN, "fixed": True, "answer": 1},
            {"text": "Most of the students had visited Kazan before.", "options": TFN, "fixed": True, "answer": 1},
            {"text": "The students tried traditional food in a café.", "options": TFN, "fixed": True, "answer": 0},
            {"text": "The trip cost a lot of money.", "options": TFN, "fixed": True, "answer": 2},
        ],
    },
    "read_hard": {
        "kind": "reading",
        "intro": "📖 <b>Чтение, задание 2</b> (формат ЕГЭ)\n\nПрочитайте статью и ответьте на 4 вопроса.",
        "text": (
            "<b>Teenagers and Sleep</b>\n\n"
            "For years, parents and teachers have complained that teenagers are lazy because they find it so hard to "
            "get up in the morning. Scientists, however, now believe that the problem is largely biological. During "
            "adolescence, the body begins to produce melatonin, the hormone that makes us feel sleepy, about two "
            "hours later than it does in children and adults. As a result, a typical teenager is simply not ready to "
            "fall asleep before eleven o'clock at night, yet school often starts at eight.\n\n"
            "Some schools in the USA have experimented with later start times, and the results have been "
            "encouraging: attendance has risen, and students report feeling more alert in class. Critics argue that "
            "later starts would cause problems for parents' work schedules and after-school activities, but "
            "supporters insist that students' health should come first."
        ),
        "questions": [
            {"text": "According to scientists, why do teenagers find it hard to get up early?",
             "options": ["Their bodies produce melatonin later", "They are lazy",
                         "They use their phones at night", "They have too much homework"]},
            {"text": "When is a typical teenager ready to fall asleep?",
             "options": ["Not before 11 p.m.", "At about 9 p.m.", "At about 10 p.m.", "Right after school"]},
            {"text": "What happened in schools that started later?",
             "options": ["Students came to school more regularly", "Students got worse marks",
                         "Teachers left the schools", "After-school clubs were closed"]},
            {"text": "\"Students' health should come first\" means that...",
             "options": ["health is more important than other concerns",
                         "students should see a doctor before school",
                         "healthy students should start lessons first",
                         "health lessons should be the first lesson"]},
        ],
    },
}

# ---- Блок в PDF ----
# Какой уровень нужен для экзамена (ориентировочно)
TARGETS = {"ОГЭ": ("B1", "на «5» обычно нужен уровень A2+–B1"),
           "ЕГЭ": ("B2", "на 80+ баллов обычно нужен уровень B1+–B2")}

RECS = {
    "title": "Ваша цель: сдать экзамен",
    "tips": [
        "Начните с демоверсии ФИПИ: она показывает точный формат заданий и критерии оценки.",
        "Раз в 2–3 недели решайте полный вариант на время, остальное время закрывайте слабые места.",
        "Грамматику и словообразование учите блоками: времена, пассив, суффиксы прилагательных и существительных.",
        "Письмо и устная часть дают много баллов: учите структуру ответа и тренируйтесь с проверкой учителя.",
        "Читайте и слушайте английский не только по сборникам: сериалы и книги расширяют словарь быстрее.",
    ],
    "resources": [
        "Демоверсии и открытый банк заданий на сайте ФИПИ (fipi.ru).",
        "Сборники М. В. Вербицкой (ОГЭ и ЕГЭ).",
        "Macmillan «Exam Skills for Russia»: отдельные книги по грамматике и чтению.",
    ],
}
