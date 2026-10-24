# Тест «Для работы»: офис, встречи, письма, переговоры.
# Первый вариант ответа в каждом вопросе - правильный, бот перемешивает варианты сам.

# ---- Часть 1. Грамматика и лексика ----
# На каждый уровень 4 вопроса: 2 на грамматику и 2 на лексику ("lexis": True).
GRAMMAR = {
    "A1": [
        {"text": "I ___ a manager in a big company.", "options": ["am", "is", "are", "be"]},
        {"text": "I have a ___ with my boss at 10 a.m.", "options": ["meeting", "lesson", "party", "holiday"], "lexis": True},
        {"text": "She ___ in an office in the city centre.", "options": ["works", "work", "working", "is work"]},
        {"text": "Please send me an ___ with the details.", "options": ["email", "office", "phone", "desk"], "lexis": True},
    ],
    "A2": [
        {"text": "I ___ an email to the client yesterday.", "options": ["sent", "send", "have sent", "sended"]},
        {"text": "She ___ a lot of money in her new job.", "options": ["earns", "wins", "gains", "pays"], "lexis": True},
        {"text": "She's busy at the moment. She ___ to a customer.", "options": ["is talking", "talks", "talk", "talked"]},
        {"text": "Our company ___ 200 people.", "options": ["employs", "works", "makes", "does"], "lexis": True},
    ],
    "B1": [
        {"text": "I've worked for this company ___ 2019.", "options": ["since", "for", "from", "during"]},
        {"text": "Could you ___ me a favour and check this presentation?", "options": ["do", "make", "give", "take"], "lexis": True},
        {"text": "If the client ___ the contract, we'll start next week.", "options": ["signs", "will sign", "signed", "would sign"]},
        {"text": "I'd like to ___ for the position of sales manager.", "options": ["apply", "ask", "request", "offer"], "lexis": True},
    ],
    "B2": [
        {"text": "I wish I ___ that job offer last year.", "options": ["had accepted", "accepted", "would accept", "have accepted"]},
        {"text": "The meeting has been ___ until next Monday because the director is away.", "options": ["postponed", "cancelled", "prevented", "avoided"], "lexis": True},
        {"text": "She's been promoted, ___ means she'll have more responsibilities.", "options": ["which", "that", "what", "who"]},
        {"text": "We must ___ the deadline, or the client will be unhappy.", "options": ["meet", "catch", "win", "follow"], "lexis": True},
    ],
    "C1": [
        {"text": "Under no circumstances ___ confidential information with third parties.", "options": ["should employees share", "employees should share", "should share employees", "employees share"]},
        {"text": "We're looking for someone who can ___ the initiative and work independently.", "options": ["take", "make", "get", "do"], "lexis": True},
        {"text": "Had the market not collapsed, the merger ___ ahead.", "options": ["would have gone", "had gone", "went", "will have gone"]},
        {"text": "Her proposal was met with ___ approval from the board.", "options": ["unanimous", "unanimously", "unanimity", "unanimousness"], "lexis": True},
    ],
}

# ---- Части 2 и 3. Аудирование и чтение ----
TASKS = {
    "listen_easy": {
        "kind": "listening",
        "voice": "am_michael", "speed": 0.88,
        "intro": "🎧 <b>Часть 2. Аудирование</b>\n\nПослушай голосовое сообщение от партнёра "
                 "и ответь на 4 вопроса. Можно слушать несколько раз.",
        "script": (
            "Hello, this is David Green from Northstar Logistics. I'm calling about our meeting on Tuesday. "
            "I'm afraid I can't make it in the morning, because I have to visit a customer. "
            "Could we move it to Wednesday at two o'clock instead? I'll bring the new price list with me. "
            "If Wednesday doesn't work for you, please send me an email, and we can find another time. "
            "Thanks, bye."
        ),
        "questions": [
            {"text": "Why is David calling?",
             "options": ["To move a meeting", "To cancel an order", "To ask for a price list", "To book a hotel"]},
            {"text": "Why can't he meet on Tuesday morning?",
             "options": ["He has to visit a customer", "He is ill", "He is on holiday", "He has a meeting at his office"]},
            {"text": "When does he want to meet?",
             "options": ["Wednesday at 2 p.m.", "Tuesday at 2 p.m.", "Wednesday morning", "Thursday at 2 p.m."]},
            {"text": "What should you do if Wednesday isn't convenient?",
             "options": ["Send him an email", "Call his office", "Come on Tuesday", "Wait for his call"]},
        ],
    },
    "listen_hard": {
        "kind": "listening",
        "voice": "af_heart", "speed": 1.0,
        "intro": "🎧 <b>Часть 2. Аудирование</b>\n\nРуководитель делится опытом "
                 "в обычном темпе. Ответь на 4 вопроса.",
        "script": (
            "One of the biggest mistakes I see new managers make is assuming that their job is to have all the "
            "answers. It isn't. In fact, the moment you start solving every problem yourself, your team stops "
            "thinking. What I've found works much better is asking questions. What do you think we should do? What "
            "options have you considered? At first it feels slower, and frankly, it can be frustrating when you can "
            "see the solution and they can't. But within a few months, people start coming to you with solutions "
            "rather than problems, and that frees you up to focus on the bigger picture."
        ),
        "questions": [
            {"text": "What mistake do new managers often make?",
             "options": ["They think they must have all the answers", "They ask too many questions",
                         "They don't trust their bosses", "They work too slowly"]},
            {"text": "What happens when a manager solves every problem?",
             "options": ["The team stops thinking for itself", "The team works faster",
                         "The manager gets promoted", "Customers complain"]},
            {"text": "How does the speaker feel about asking questions at first?",
             "options": ["It can be frustrating", "It's quick and easy", "It's unnecessary", "It's embarrassing"]},
            {"text": "What is the long-term benefit of this approach?",
             "options": ["The team brings solutions and the manager can see the bigger picture",
                         "The manager can work fewer hours", "The company needs fewer people",
                         "Meetings become shorter"]},
        ],
    },
    "read_easy": {
        "kind": "reading",
        "intro": "📖 <b>Часть 3. Чтение</b>\n\nПрочитай рабочее письмо и ответь на 4 вопроса.",
        "text": (
            "Hi team,\n"
            "\n"
            "On Monday we have a visit from our new clients from Germany, so please come to the office by 9 a.m. "
            "instead of 10. Lunch will be provided, so you don't need to bring your own. On Friday the office "
            "will close early, at 3 p.m., because of electrical work in the building.\n"
            "\n"
            "Best regards,\n"
            "Mark"
        ),
        "questions": [
            {"text": "Why should the team come in early on Monday?",
             "options": ["New clients are visiting", "There is electrical work",
                         "There is a training course", "Olga is leaving"]},
            {"text": "What time should people arrive on Monday?",
             "options": ["9 a.m.", "10 a.m.", "3 p.m.", "8 a.m."]},
            {"text": "What does Mark say about lunch?",
             "options": ["Staff don't need to bring their own", "Staff should bring their own",
                         "There is no lunch break", "Lunch will be at 3 p.m."]},
            {"text": "Why will the office close early on Friday?",
             "options": ["Because of electrical work", "Because of the clients' visit",
                         "Because it's a holiday", "Because Mark is away"]},
        ],
    },
    "read_hard": {
        "kind": "reading",
        "intro": "📖 <b>Часть 3. Чтение</b>\n\nПрочитай статью и ответь на 4 вопроса.",
        "text": (
            "<b>Is the Office Dead?</b>\n"
            "\n"
            "When the pandemic sent millions of employees home, many predicted that the traditional office would "
            "never recover. Several years on, the picture is more complicated. Surveys show that most employees "
            "value the flexibility of remote work. At the same time, some large companies have called staff back,"
            " arguing that creativity and team spirit suffer when colleagues never meet. Many organisations have "
            "chosen a hybrid model, with part of the week at home and part in the office. Whether this will last "
            "remains to be seen."
        ),
        "questions": [
            {"text": "What did many people predict during the pandemic?",
             "options": ["The traditional office would not recover", "Everyone would quickly return to the office",
                         "Most companies would close", "People would work longer hours"]},
            {"text": "What do surveys show about employees?",
             "options": ["Most value being able to work flexibly", "Most prefer working in the office",
                         "Most want to work longer hours", "Most want to change jobs"]},
            {"text": "Why have some companies called staff back to the office?",
             "options": ["They think creativity and team spirit suffer", "Offices are cheaper",
                         "Employees asked for it", "Remote work is too expensive"]},
            {"text": "What does the writer say about the hybrid model?",
             "options": ["It is not yet clear whether it will last", "It is the perfect solution",
                         "It has already failed", "Very few companies use it"]},
        ],
    },
}

# ---- Блок в PDF ----
RECS = {
    "title": "Твоя цель: английский для работы",
    "tips": [
        "Начни с того, что нужно каждый день: письма, созвоны, рассказ о своей работе и проектах.",
        "Собери шаблоны деловых фраз: договориться о встрече, перенести её, вежливо не согласиться, подвести итог.",
        "Учи лексику своей сферы: 50-100 профессиональных слов дадут больше, чем общий словарь.",
        "Тренируй small talk: короткий разговор перед встречей сильно влияет на впечатление о тебе.",
    ],
    "resources": [
        "BBC Learning English: «English at Work», «Business English».",
        "Подкаст «Business English Pod».",
        "Книга «Business Vocabulary in Use» (Cambridge).",
    ],
}
