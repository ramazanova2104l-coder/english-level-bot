# Тест «Разговорный английский» (и «Просто интересно»): повседневные темы.
# Первый вариант ответа в каждом вопросе - правильный, бот перемешивает варианты сам.

# ---- Часть 1. Грамматика и лексика ----
GRAMMAR = {
    "A1": [
        {"text": "My sister ___ two children.", "options": ["has", "have", "is", "are"]},
        {"text": "___ is your name?", "options": ["What", "Who", "Where", "How"]},
        {"text": "They ___ from Spain.", "options": ["are", "is", "am", "be"]},
        {"text": "I usually ___ up at 7 o'clock.", "options": ["get", "gets", "getting", "got"]},
        {"text": "I have ___ apple and a banana.", "options": ["an", "a", "some", "any"]},
    ],
    "A2": [
        {"text": "We ___ to Italy last summer.", "options": ["went", "have gone", "go", "are going"]},
        {"text": "She can't come to the phone. She ___ a shower.",
         "options": ["is having", "has", "have", "had"]},
        {"text": "This is the ___ film I've ever seen.",
         "options": ["best", "better", "most good", "goodest"]},
        {"text": "There isn't ___ milk in the fridge.", "options": ["any", "some", "many", "a"]},
        {"text": "I'm very ___ in history, so I often visit museums.",
         "options": ["interested", "interesting", "interest", "interests"]},
    ],
    "B1": [
        {"text": "I've lived here ___ five years.", "options": ["for", "since", "during", "from"]},
        {"text": "If I ___ more money, I would buy a car.",
         "options": ["had", "have", "will have", "would have"]},
        {"text": "A new hospital ___ in our town next year.",
         "options": ["will be built", "will build", "is building", "builds"]},
        {"text": "I'm looking forward ___ you.",
         "options": ["to seeing", "to see", "seeing", "for seeing"]},
        {"text": "You ___ wear a uniform at our school. It's optional.",
         "options": ["don't have to", "mustn't", "can't", "haven't"]},
    ],
    "B2": [
        {"text": "I'd rather you ___ smoke in the house.", "options": ["didn't", "don't", "won't", "not"]},
        {"text": "By next June, I ___ here for ten years.",
         "options": ["will have worked", "will work", "am working", "have worked"]},
        {"text": "She denied ___ the money.", "options": ["taking", "to take", "take", "to taking"]},
        {"text": "Despite ___ tired, he kept working.", "options": ["being", "he was", "to be", "be"]},
        {"text": "I can't ___ up with this noise any longer.", "options": ["put", "take", "get", "make"]},
    ],
    "C1": [
        {"text": "Little ___ that the police were watching him.",
         "options": ["did he know", "he knew", "he did know", "knew he"]},
        {"text": "Had I known about the problem, I ___ something.",
         "options": ["would have done", "had done", "did", "will have done"]},
        {"text": "The plan was rejected on the ___ that it was too expensive.",
         "options": ["grounds", "reasons", "terms", "causes"]},
        {"text": "She's ___ the best candidate we've interviewed.",
         "options": ["by far", "very", "much more", "far more"]},
        {"text": "Scarcely had we sat down ___ the phone rang.",
         "options": ["when", "than", "that", "then"]},
    ],
}

# ---- Части 2 и 3. Аудирование и чтение ----
TASKS = {
    "listen_easy": {
        "kind": "listening",
        "voice": "af_bella", "speed": 0.85,
        "intro": "🎧 <b>Аудирование, задание 1</b>\n\nПослушай голосовое сообщение и ответь на 4 вопроса. "
                 "Можно слушать несколько раз.",
        "script": (
            "Hi Sam, it's Maria. I'm calling about Saturday. I'm really sorry, but I can't meet you at six, "
            "because I have to work until half past five. Can we meet at seven instead? "
            "Actually, no. The film starts at a quarter past seven, and we still need to buy tickets. "
            "Let's say a quarter to seven, outside the cinema. "
            "Oh, and my brother Tom wants to come with us. Is that OK? "
            "Don't worry, he says he'll pay for the popcorn! Call me back when you get this. Bye!"
        ),
        "questions": [
            {"text": "Why is Maria calling?",
             "options": ["To change the time they meet", "To cancel the film",
                         "To invite Sam to her work", "To ask Sam to buy the tickets"]},
            {"text": "What time will they meet now?",
             "options": ["At a quarter to seven", "At seven", "At six", "At a quarter past seven"]},
            {"text": "Where will they meet?",
             "options": ["Outside the cinema", "At Maria's work", "At Maria's house", "Inside the cinema"]},
            {"text": "What does Tom offer to do?",
             "options": ["Pay for the popcorn", "Buy the tickets", "Drive them there", "Call Sam back"]},
        ],
    },
    "listen_hard": {
        "kind": "listening",
        "voice": "af_heart", "speed": 1.0,
        "intro": "🎧 <b>Аудирование, задание 2</b>\n\nЭто задание сложнее: отрывок из подкаста в обычном темпе. "
                 "Ответь на 4 вопроса.",
        "script": (
            "A lot of people assume that the key to learning a language is talent. You've either got it or you "
            "haven't. But the research really doesn't back that up. What seems to matter far more is how "
            "consistently you're exposed to the language, and, crucially, whether you're actually made to produce "
            "it. You can listen to podcasts for years and still freeze the moment someone asks you a question. "
            "That's not because you don't know the words. It's because retrieving them under pressure is a "
            "separate skill, and it only develops through practice. So if I had to give one piece of advice, it "
            "wouldn't be 'study more grammar'. It would be: find situations where you have no choice but to "
            "speak, even if you feel a bit uncomfortable at first."
        ),
        "questions": [
            {"text": "According to the speaker, what matters most in learning a language?",
             "options": ["Regular exposure and having to speak", "Natural talent",
                         "Learning grammar rules", "Listening to podcasts every day"]},
            {"text": "Why do some learners \"freeze\" when someone asks them a question?",
             "options": ["They haven't practised finding words under pressure",
                         "They don't know enough words", "They are naturally shy",
                         "They have listened to too many podcasts"]},
            {"text": "What does the speaker think about the idea that language learning depends on talent?",
             "options": ["It isn't supported by evidence", "It is partly true",
                         "It is true for adults only", "She hasn't decided yet"]},
            {"text": "What does the speaker advise learners to do?",
             "options": ["Put themselves in situations where they must speak",
                         "Avoid feeling uncomfortable", "Study grammar more carefully",
                         "Listen for a long time before speaking"]},
        ],
    },
    "read_easy": {
        "kind": "reading",
        "intro": "📖 <b>Чтение, задание 1</b>\n\nПрочитай короткую статью и ответь на 4 вопроса.",
        "text": (
            "<b>Little Free Libraries</b>\n\n"
            "In many towns around the world, you can find small wooden boxes standing in front of people's houses. "
            "They look like birdhouses, but they are full of books. These are called Little Free Libraries. The "
            "idea is simple: you take a book you want to read and leave a book you have already finished. Nobody "
            "pays any money, and there are no rules about when you have to bring a book back.\n\n"
            "The first one was built in the USA in 2009 by a man called Todd Bol, in memory of his mother, a "
            "teacher who loved reading. Today there are more than 150,000 of them in over a hundred countries. "
            "Many owners say that the boxes have helped them get to know their neighbours."
        ),
        "questions": [
            {"text": "What are Little Free Libraries?",
             "options": ["Small boxes of books outside people's houses", "Houses for birds",
                         "Big libraries in town centres", "Second-hand bookshops"]},
            {"text": "What should you do when you take a book?",
             "options": ["Leave another book", "Pay a little money",
                         "Bring it back within a week", "Write your name in it"]},
            {"text": "Why did Todd Bol build the first one?",
             "options": ["In memory of his mother", "To sell his old books",
                         "For the school where he worked", "To make his house look nicer"]},
            {"text": "What do many owners say about the boxes?",
             "options": ["They have helped them meet their neighbours", "They earn money from them",
                         "People often steal the books", "They are expensive to build"]},
        ],
    },
    "read_hard": {
        "kind": "reading",
        "intro": "📖 <b>Чтение, задание 2</b>\n\nЭтот текст сложнее. Прочитай его и ответь на 4 вопроса.",
        "text": (
            "<b>The Myth of Multitasking</b>\n\n"
            "Many of us take pride in our ability to juggle several tasks at once: answering emails during "
            "meetings, scrolling through the news while on the phone. Yet a growing body of research suggests "
            "that what we call multitasking is, in fact, rapid switching between tasks, and that each switch "
            "carries a cost. Studies have found that people who habitually multitask perform worse on tests of "
            "attention and memory than those who tend to focus on one thing at a time. Perhaps more "
            "surprisingly, heavy multitaskers often rate their own abilities highly, which may explain why the "
            "habit is so hard to break.\n\n"
            "None of this means that we should never do two things at once; listening to music while cooking "
            "is unlikely to cause problems. The difficulty arises when both tasks demand our full attention."
        ),
        "questions": [
            {"text": "According to the text, what is multitasking really?",
             "options": ["Switching quickly between tasks", "Doing two things with equal attention",
                         "A skill that improves with practice", "A problem caused by modern technology"]},
            {"text": "What did studies find about people who often multitask?",
             "options": ["They did worse on attention and memory tests", "They had better memories",
                         "They worked faster than others", "They rarely answered emails"]},
            {"text": "Why might the multitasking habit be \"so hard to break\"?",
             "options": ["Heavy multitaskers overestimate their abilities", "Technology makes it necessary",
                         "People find it enjoyable", "Employers expect it"]},
            {"text": "What is the writer's overall position?",
             "options": ["It is a problem mainly when both tasks need full attention",
                         "We should never do two things at once",
                         "It is harmless for most people",
                         "Listening to music harms concentration"]},
        ],
    },
}

# ---- Блок в PDF ----
RECS = {
    "title": "Твоя цель: свободно говорить",
    "tips": [
        "Говори каждый день, хотя бы 5-10 минут: вслух пересказывай, что прочитали или посмотрели.",
        "Учи не отдельные слова, а готовые фразы и реакции: «That makes sense», «I see what you mean».",
        "Записывай себя на диктофон и переслушивай: так легче заметить паузы и ошибки.",
        "Регулярная практика с живым собеседником (уроки, Speaking Club) даёт больше, чем месяцы приложений.",
    ],
}
