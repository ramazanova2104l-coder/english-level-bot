# Тест «Для путешествий»: аэропорт, отель, город, общение в поездке.
# Первый вариант ответа в каждом вопросе — правильный, бот перемешивает варианты сам.

# ---- Часть 1. Грамматика и лексика ----
GRAMMAR = {
    "A1": [
        {"text": "Excuse me, where ___ the train station?", "options": ["is", "are", "am", "be"]},
        {"text": "I'd like ___ coffee, please.", "options": ["a", "an", "any", "many"]},
        {"text": "How ___ is this ticket?", "options": ["much", "many", "old", "far"]},
        {"text": "Hello, we ___ a reservation for two nights.", "options": ["have", "has", "are", "is"]},
        {"text": "The museum opens ___ 9 a.m.", "options": ["at", "in", "on", "to"]},
    ],
    "A2": [
        {"text": "Last year we ___ to Turkey.", "options": ["flew", "flied", "have flown", "fly"]},
        {"text": "Excuse me, ___ I have the bill, please?", "options": ["could", "do", "am", "will"]},
        {"text": "This hotel is ___ than the one we stayed in last year.",
         "options": ["cheaper", "more cheap", "cheapest", "cheaply"]},
        {"text": "We ___ to Paris next month. We've already bought the tickets.",
         "options": ["are going", "go", "went", "goes"]},
        {"text": "Our flight was ___ because of the bad weather.",
         "options": ["cancelled", "cancelling", "cancel", "cancels"]},
    ],
    "B1": [
        {"text": "Have you ever ___ sushi in Japan?", "options": ["eaten", "ate", "eat", "eating"]},
        {"text": "If you ___ the 10 o'clock train, you'll arrive by noon.",
         "options": ["take", "will take", "took", "would take"]},
        {"text": "Passengers ___ smoke anywhere on the plane.",
         "options": ["mustn't", "don't have to", "needn't", "haven't"]},
        {"text": "The hotel ___ we stayed was right next to the beach.",
         "options": ["where", "which", "who", "what"]},
        {"text": "We had to ___ our trip because my mother was ill.",
         "options": ["put off", "put on", "put up", "put out"]},
    ],
    "B2": [
        {"text": "If we ___ earlier, we wouldn't have missed the flight.",
         "options": ["had left", "left", "would leave", "have left"]},
        {"text": "You'd better ___ your passport in the hotel safe.",
         "options": ["leave", "to leave", "leaving", "left"]},
        {"text": "By the time we got to the gate, the plane ___.",
         "options": ["had already taken off", "already took off", "has already taken off", "was already taking off"]},
        {"text": "I'm not used to ___ on the left side of the road.",
         "options": ["driving", "drive", "drove", "be driving"]},
        {"text": "The guide ___ us that the castle was closed for repairs.",
         "options": ["informed", "said", "explained", "spoke"]},
    ],
    "C1": [
        {"text": "Not only ___ our luggage, but they also overbooked our flight.",
         "options": ["did they lose", "they lost", "lost they", "they did lose"]},
        {"text": "The hotel was nothing ___ the photos on the website. It was far worse.",
         "options": ["like", "as", "than", "similar"]},
        {"text": "Should you ___ any problems during your stay, please contact reception.",
         "options": ["have", "had", "having", "to have"]},
        {"text": "The old town is well worth ___.", "options": ["visiting", "to visit", "visit", "visited"]},
        {"text": "Travellers are advised to ___ caution when using public transport late at night.",
         "options": ["exercise", "do", "make", "give"]},
    ],
}

# ---- Части 2 и 3. Аудирование и чтение ----
TASKS = {
    "listen_easy": {
        "kind": "listening",
        "voice": "af_bella", "speed": 0.88,
        "intro": "🎧 <b>Аудирование, задание 1</b>\n\nПослушайте объявление в аэропорту и ответьте на 4 вопроса. "
                 "Можно слушать несколько раз.",
        "script": (
            "Attention, please. This is an announcement for passengers on flight B A two seven four to London. "
            "Unfortunately, the flight has been delayed by forty-five minutes because of bad weather. "
            "The new departure time is eleven fifteen. "
            "Boarding will now take place at gate twelve, not gate eight. "
            "Passengers with small children may board first. "
            "We apologise for any inconvenience. Thank you."
        ),
        "questions": [
            {"text": "Where is the flight going?", "options": ["London", "Paris", "Berlin", "Dublin"]},
            {"text": "Why is the flight delayed?",
             "options": ["Because of bad weather", "Because of a technical problem",
                         "Because the pilot is late", "Because of a strike"]},
            {"text": "What is the new departure time?", "options": ["11:15", "10:30", "11:45", "12:00"]},
            {"text": "Where will boarding take place?", "options": ["Gate 12", "Gate 8", "Gate 2", "Gate 20"]},
        ],
    },
    "listen_hard": {
        "kind": "listening",
        "voice": "af_heart", "speed": 1.0,
        "intro": "🎧 <b>Аудирование, задание 2</b>\n\nЭто задание сложнее: тревел-блогер рассказывает о своих "
                 "поездках в обычном темпе. Ответьте на 4 вопроса.",
        "script": (
            "People often ask me how I manage to travel so much on such a small budget. The honest answer is that "
            "I've stopped trying to see everything. When I first started travelling, I'd rush from one famous sight "
            "to the next, ticking things off a list, and I'd come home exhausted and, frankly, with very few real "
            "memories. These days I'll pick one neighbourhood and stay there for a week. I rent a small flat instead "
            "of a hotel, I shop at the local market, and I eat wherever the locals eat. Not only does it work out "
            "much cheaper, but I actually get to talk to people. Some of my best travel moments have come from a "
            "conversation with a shop owner, not from a museum."
        ),
        "questions": [
            {"text": "What was the problem with the speaker's early trips?",
             "options": ["She tried to see too much and remembered little", "They were too expensive",
                         "She always travelled alone", "She stayed in bad hotels"]},
            {"text": "How does the speaker travel now?",
             "options": ["She stays in one area for longer", "She visits more famous sights",
                         "She only stays in hotels", "She travels with a tour group"]},
            {"text": "What are the benefits of living like a local, according to her?",
             "options": ["It's cheaper and she meets people", "The food is healthier",
                         "She doesn't have to cook", "She can visit more museums"]},
            {"text": "What does the speaker suggest about museums?",
             "options": ["They are often less memorable than meeting locals", "They are too expensive",
                         "They are always crowded", "She never visits them"]},
        ],
    },
    "read_easy": {
        "kind": "reading",
        "intro": "📖 <b>Чтение, задание 1</b>\n\nПрочитайте информацию об отеле и ответьте на 4 вопроса.",
        "text": (
            "<b>Sea View Hotel</b>\n\n"
            "Our family hotel is just five minutes' walk from the beach. All rooms have free Wi-Fi, a fridge and a "
            "balcony. Breakfast is served from 7 to 10 a.m. in the garden restaurant and is included in the price. "
            "Dinner is available for an extra charge. Check-in is from 2 p.m., and check-out is before 11 a.m. If "
            "you arrive early, you can leave your bags at reception and go to the beach. We are happy to book taxis "
            "and boat trips for our guests. Please note that pets are not allowed."
        ),
        "questions": [
            {"text": "How far is the hotel from the beach?",
             "options": ["Five minutes on foot", "Five minutes by car", "It's on the beach", "Fifteen minutes on foot"]},
            {"text": "What is included in the price?", "options": ["Breakfast", "Dinner", "Boat trips", "Taxis"]},
            {"text": "What can guests do if they arrive before 2 p.m.?",
             "options": ["Leave their bags at reception", "Go straight to their room",
                         "Have a free dinner", "Check out early"]},
            {"text": "Which of these is true?",
             "options": ["You can't bring your dog", "Rooms don't have Wi-Fi",
                         "Breakfast is served until 11 a.m.", "The hotel can't book taxis"]},
        ],
    },
    "read_hard": {
        "kind": "reading",
        "intro": "📖 <b>Чтение, задание 2</b>\n\nЭтот текст сложнее. Прочитайте статью и ответьте на 4 вопроса.",
        "text": (
            "<b>The Price of Popularity</b>\n\n"
            "Venice, Barcelona and Amsterdam have something in common: they are struggling with what has come to be "
            "known as overtourism. Every year, millions of visitors pour into their historic centres, pushing up "
            "rents and forcing many long-term residents to move out. In some neighbourhoods, shops selling everyday "
            "goods have been replaced by souvenir stalls, and locals complain that their city is turning into a "
            "theme park.\n\n"
            "City authorities have responded in different ways. Venice has introduced an entry fee for day-trippers, "
            "while Amsterdam has banned new hotels in the city centre. Critics of such measures argue that they "
            "penalise ordinary travellers and do little to address the real causes: cheap flights and short-term "
            "rental platforms. What is clear is that the tourism model of the last few decades cannot simply "
            "continue unchanged."
        ),
        "questions": [
            {"text": "What problem do Venice, Barcelona and Amsterdam share?",
             "options": ["Too many tourists", "Too few hotels", "Expensive flights", "Bad weather"]},
            {"text": "How has overtourism affected local residents?",
             "options": ["Many have had to leave because of high rents", "They have opened souvenir shops",
                         "They have become richer", "They have moved into the centre"]},
            {"text": "What do critics say about measures like entry fees?",
             "options": ["They don't deal with the main causes", "They are too cheap",
                         "They have solved the problem", "They only help hotels"]},
            {"text": "What is the writer's conclusion?",
             "options": ["Tourism has to change", "Cities should ban tourists completely",
                         "Entry fees are the best solution", "Overtourism is exaggerated"]},
        ],
    },
}

# ---- Блок в PDF ----
RECS = {
    "title": "Ваша цель: английский для путешествий",
    "tips": [
        "Соберите свой разговорник из 30–40 фраз: аэропорт, отель, кафе, магазин, как пройти, если что-то случилось.",
        "Тренируйте понимание на слух объявлений и быстрой речи: в поездке переспросить можно не всегда.",
        "Перед поездкой проиграйте ситуации вслух: заселение, заказ еды, жалоба на номер, вызов такси.",
        "Учите вежливые формы: Could I…? Would you mind…? I was wondering if… Они звучат естественно и мягко.",
    ],
    "resources": [
        "YouTube: «Easy English», уличные интервью с субтитрами.",
        "Подкаст «Travel English» и BBC Learning English, раздел «English at Work / Travel».",
        "Блоги и видео путешественников на английском о стране, куда вы едете.",
    ],
}
