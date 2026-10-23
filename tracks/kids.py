# Тест «Для ребёнка»: школа, семья, животные, хобби.
# Первый вариант ответа в каждом вопросе — правильный, бот перемешивает варианты сам.

# ---- Часть 1. Грамматика и лексика ----
GRAMMAR = {
    "A1": [
        {"text": "I ___ ten years old.", "options": ["am", "is", "are", "be"]},
        {"text": "My cat ___ fish.", "options": ["likes", "like", "liking", "is like"]},
        {"text": "Look at ___ birds in the tree!", "options": ["those", "that", "this", "it"]},
        {"text": "We ___ English on Mondays.", "options": ["have", "has", "having", "is have"]},
        {"text": "Can you ___ a bike?", "options": ["ride", "rides", "riding", "to ride"]},
    ],
    "A2": [
        {"text": "Yesterday I ___ my grandma.", "options": ["visited", "visit", "visits", "visiting"]},
        {"text": "An elephant is ___ than a horse.", "options": ["bigger", "more big", "biggest", "bigest"]},
        {"text": "Shh! The baby ___.", "options": ["is sleeping", "sleeps", "sleep", "slept"]},
        {"text": "There ___ any bread left.", "options": ["isn't", "aren't", "not", "don't"]},
        {"text": "We're going ___ the zoo on Saturday.", "options": ["to", "at", "in", "on"]},
    ],
    "B1": [
        {"text": "I've ___ finished my homework!", "options": ["just", "yet", "ever", "since"]},
        {"text": "If you ___ hard, you'll pass the test.",
         "options": ["study", "will study", "studied", "studies"]},
        {"text": "Our school ___ in 1975.", "options": ["was built", "built", "is built", "has built"]},
        {"text": "I'm good ___ drawing.", "options": ["at", "in", "on", "for"]},
        {"text": "You ___ run in the corridor! It's dangerous.",
         "options": ["mustn't", "don't have to", "needn't", "doesn't"]},
    ],
    "B2": [
        {"text": "This is the boy ___ dog bit me.", "options": ["whose", "who", "which", "that"]},
        {"text": "He asked me ___ I liked pizza.", "options": ["if", "that", "what", "do"]},
        {"text": "We'd better ___ now, or we'll miss the bus.",
         "options": ["leave", "to leave", "leaving", "left"]},
        {"text": "I've been learning English ___ I was six.", "options": ["since", "for", "from", "when"]},
        {"text": "If I had studied harder, I ___ the test.",
         "options": ["would have passed", "would pass", "passed", "will pass"]},
    ],
    "C1": [
        {"text": "Never ___ such a beautiful sunset.",
         "options": ["have I seen", "I have seen", "I saw", "saw I"]},
        {"text": "I'm not used ___ up so early.", "options": ["to getting", "to get", "getting", "get"]},
        {"text": "She's ___ the best student in our class.", "options": ["by far", "very", "much more", "so"]},
        {"text": "Our teacher made us ___ the poem by heart.",
         "options": ["learn", "to learn", "learning", "learned"]},
        {"text": "It's no use ___ about the test now. It's over.",
         "options": ["worrying", "to worry", "worry", "worried"]},
    ],
}

# ---- Части 2 и 3. Аудирование и чтение ----
TASKS = {
    "listen_easy": {
        "kind": "listening",
        "voice": "am_puck", "speed": 0.85,
        "intro": "🎧 <b>Аудирование, задание 1</b>\n\nПослушай рассказ мальчика о его собаке и ответь на 4 вопроса. "
                 "Можно слушать несколько раз.",
        "script": (
            "Hi! My name's Ben, and I'm eleven. I want to tell you about my dog, Max. "
            "He's three years old, and he's very big and brown. "
            "Every morning before school, I take him for a walk in the park. "
            "Max loves playing with balls, but he's scared of cats! "
            "On Saturdays my dad and I take him to the river, and he swims there. "
            "Max sleeps in the kitchen, but sometimes he jumps onto my bed at night."
        ),
        "questions": [
            {"text": "How old is Max?", "options": ["Three", "Eleven", "Two", "Five"]},
            {"text": "When does Ben walk Max?",
             "options": ["Every morning before school", "Every evening", "Only on Saturdays", "After lunch"]},
            {"text": "What is Max scared of?", "options": ["Cats", "Balls", "Water", "The park"]},
            {"text": "Where does Max usually sleep?",
             "options": ["In the kitchen", "On Ben's bed", "In the garden", "In the living room"]},
        ],
    },
    "listen_hard": {
        "kind": "listening",
        "voice": "af_heart", "speed": 1.0,
        "intro": "🎧 <b>Аудирование, задание 2</b>\n\nЭто задание сложнее: школьница рассказывает о своём "
                 "научном проекте. Ответь на 4 вопроса.",
        "script": (
            "For our science project this year, my friend Lily and I decided to find out whether plants grow "
            "better with music. We took six identical plants and put three of them in a room where classical music "
            "was playing for two hours a day, and the other three in a quiet room. We gave them exactly the same "
            "amount of water and light. To be honest, we expected the music plants to grow much faster, but after "
            "a month the difference was tiny, so small that our teacher said it could just be a coincidence. We "
            "were a bit disappointed at first, but our teacher explained that an unexpected result is still a real "
            "result, and that's what science is all about."
        ),
        "questions": [
            {"text": "What did the girls want to find out?",
             "options": ["If music helps plants grow", "Which music plants like best",
                         "How much water plants need", "If plants grow better in the dark"]},
            {"text": "Why did they give all the plants the same water and light?",
             "options": ["To make the experiment fair", "Because they didn't have much water",
                         "Because the teacher told them to", "To make the plants grow faster"]},
            {"text": "What was the result?",
             "options": ["There was almost no difference", "The music plants grew much faster",
                         "The quiet plants died", "The music plants died"]},
            {"text": "What did the teacher think about the result?",
             "options": ["An unexpected result is still useful", "The experiment had failed",
                         "They should repeat it with louder music", "The girls had made a mistake"]},
        ],
    },
    "read_easy": {
        "kind": "reading",
        "intro": "📖 <b>Чтение, задание 1</b>\n\nПрочитай текст и ответь на 4 вопроса.",
        "text": (
            "<b>My Best Friend</b>\n\n"
            "My best friend is called Sofia. We are in the same class at school, and we sit together. Sofia has long "
            "dark hair and green eyes. She is very funny and always makes me laugh. After school we often go to the "
            "park or play computer games at her house. Sofia loves animals, and she has two rabbits and a parrot. "
            "Her parrot can say \"hello\" and \"good night\"! At the weekend we sometimes go swimming together. "
            "I'm happy that Sofia is my friend."
        ),
        "questions": [
            {"text": "Where do the friends sit at school?",
             "options": ["Together", "Next to the teacher", "At the back", "In different classes"]},
            {"text": "What does Sofia look like?",
             "options": ["She has long dark hair and green eyes", "She has short fair hair",
                         "She has blue eyes", "She has long fair hair"]},
            {"text": "What pets does Sofia have?",
             "options": ["Two rabbits and a parrot", "A dog and a cat", "Two parrots", "A rabbit and a dog"]},
            {"text": "What can the parrot do?",
             "options": ["Say two phrases", "Sing songs", "Count to ten", "Dance"]},
        ],
    },
    "read_hard": {
        "kind": "reading",
        "intro": "📖 <b>Чтение, задание 2</b>\n\nЭтот текст сложнее. Прочитай историю и ответь на 4 вопроса.",
        "text": (
            "<b>The Boy Who Harnessed the Wind</b>\n\n"
            "When William Kamkwamba was fourteen, a terrible drought hit his village in Malawi. His family could no "
            "longer afford to pay for school, so William had to leave. Instead of giving up on learning, he started "
            "visiting the village library, where he found an old science book about energy. Although his English was "
            "limited, he studied the diagrams carefully and decided to build a windmill to produce electricity.\n\n"
            "Using old bicycle parts, plastic pipes and wood, he eventually built a working windmill that powered a "
            "few lights in his home. At first, some neighbours laughed at him and thought he had gone mad. Later, "
            "when they saw what he had achieved, many of them came to charge their phones at his house. William's "
            "story became famous around the world, and he was later able to continue his education."
        ),
        "questions": [
            {"text": "Why did William have to leave school?",
             "options": ["His family couldn't pay for it", "He was ill", "He failed his exams",
                         "He moved to another country"]},
            {"text": "How did William learn to build a windmill?",
             "options": ["From a book in the library", "From his teacher", "From the internet",
                         "From his neighbours"]},
            {"text": "How did the neighbours' attitude change?",
             "options": ["At first they laughed, later they used his electricity", "They always supported him",
                         "They became angry with him", "They never noticed the windmill"]},
            {"text": "What does William's story show?",
             "options": ["You can keep learning even in difficult times", "You need a lot of money to build things",
                         "Windmills are easy to build", "Libraries are not useful"]},
        ],
    },
}

# ---- Блок в PDF ----
RECS = {
    "title": "Английский для ребёнка",
    "tips": [
        "Короткие, но регулярные занятия: 15–20 минут в день работают лучше, чем час раз в неделю.",
        "Английский через то, что ребёнку уже интересно: мультфильмы, игры, песни, любимые герои.",
        "Хвалите за попытку сказать, а не только за правильность: страх ошибки мешает заговорить.",
        "Школьную программу полезно опережать на полшага: тогда уроки в школе даются легко.",
    ],
    "resources": [
        "Мультфильмы и сериалы на английском: «Peppa Pig», «Bluey», «Gravity Falls» (для старших).",
        "Адаптированные книги Oxford Read and Discover, Penguin Kids Readers.",
        "Приложения с играми для детей: Lingokids (для младших).",
    ],
}
