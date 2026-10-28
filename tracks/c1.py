# Бонусный блок C1: общий для всех целей.
# Его получает только тот, кто прошёл весь тест без ошибок (грамматика B2 и C1 4 из 4,
# сложные аудио и текст 4 из 4). Уровень C1 ставится, если и здесь почти всё верно.
# Аудио лежит в media/listen_c1.mp3 (одно на все цели).

TASKS = {
    "listen_c1": {
        "kind": "listening",
        "voice": "am_michael", "speed": 1.0,
        "intro": "🔥 <b>Бонус: уровень C1</b>\n\nВесь тест без единой ошибки, поэтому открывается "
                 "бонусный блок. Здесь проверяем, есть ли у тебя C1.\n\n"
                 "🎧 Фрагмент лекции в естественном темпе, около минуты. Ответь на 4 вопроса.",
        "script": (
            "Ask people whether they understand how a zipper works, and most will say yes without hesitation. "
            "Ask them to explain it, step by step, and that confidence tends to evaporate. Psychologists call this "
            "the illusion of explanatory depth. What's striking isn't that we know so little. Nobody can be an "
            "expert in everything. It's that we so rarely notice the gap. We mistake familiarity for understanding. "
            "And the effect isn't confined to gadgets. When researchers asked people to explain, in detail, how a "
            "policy they felt strongly about would actually work, their views became noticeably more moderate. "
            "Not because anyone had argued with them, but because they'd been forced to confront the limits of "
            "their own knowledge. Now, I'd stop short of calling this a cure for polarisation. People are perfectly "
            "capable of doubling down. But it does suggest that the simple question, how exactly would that work, "
            "might do more to cool a heated debate than any counter-argument ever could."
        ),
        "questions": [
            {"text": "What is the \"illusion of explanatory depth\"?",
             "options": ["Believing we understand something better than we actually do",
                         "Being unable to explain things we have never seen",
                         "Knowing many facts but never using them",
                         "Explaining simple things in too much detail"]},
            {"text": "What does the speaker find most striking?",
             "options": ["That we rarely notice the limits of our knowledge",
                         "That most people know very little about technology",
                         "That even experts cannot explain how a zipper works",
                         "That people refuse to explain their opinions"]},
            {"text": "Why did people's views on the policy become more moderate?",
             "options": ["Explaining the details showed them how little they knew",
                         "The researchers presented strong counter-arguments",
                         "They learned new facts about the policy",
                         "They wanted to agree with the researchers"]},
            {"text": "What is the speaker's attitude to these findings?",
             "options": ["Cautiously optimistic: useful, but not a complete solution",
                         "Fully convinced they can end polarisation",
                         "Doubtful that the research is reliable",
                         "Indifferent, because the effect is too small to matter"]},
        ],
    },
    "read_c1": {
        "kind": "reading",
        "intro": "🔥 <b>Бонус: уровень C1</b>\n\n📖 Короткий авторский текст. Прочитай его внимательно, "
                 "здесь важны оттенки смысла. Ответь на 4 вопроса.",
        "text": (
            "<b>The Patience We Are Losing</b>\n"
            "\n"
            "It has become something of a truism that we live in an attention economy, in which our focus is the "
            "commodity being bought and sold. Less often remarked upon is what this does to our tolerance for "
            "difficulty. A book that does not reward us within the first few pages, an argument that takes time to "
            "unfold, a piece of music that resists easy enjoyment: all now compete, at a disadvantage, with content "
            "engineered to please instantly. The danger is not that we will stop reading altogether, but that we "
            "will gradually lose the capacity to stay with something that is not yet rewarding. Yet it is precisely "
            "that capacity, the willingness to remain uncomfortable a little longer, on which most worthwhile "
            "understanding depends."
        ),
        "questions": [
            {"text": "\"It has become something of a truism\" suggests that the idea is...",
             "options": ["so widely accepted that it is almost obvious", "controversial and rarely discussed",
                         "recently proven by scientists", "popular but clearly false"]},
            {"text": "Why do difficult books and music compete \"at a disadvantage\"?",
             "options": ["Other content is designed to give pleasure instantly",
                         "They are more expensive than other content",
                         "Fewer people are able to create them",
                         "They are rarely recommended online"]},
            {"text": "What does the writer see as the real danger?",
             "options": ["Losing the ability to persist with things that aren't immediately rewarding",
                         "People giving up reading altogether",
                         "Attention becoming too expensive to buy",
                         "Art and music becoming too simple"]},
            {"text": "Which statement best reflects the writer's view?",
             "options": ["Real understanding usually requires putting up with some discomfort",
                         "The attention economy will soon come to an end",
                         "Difficult books should be made easier to read",
                         "Anything that gives instant pleasure is harmful"]},
        ],
    },
}
