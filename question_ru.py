# Перевод вопросов на русский: бот показывает его под английским вопросом, чтобы было понятно, что делать.
# Ключ - вопрос на английском точно как в файлах tracks, значение - перевод.
# Если перевода для вопроса нет, бот просто покажет вопрос без него.

# Подсказка для вопросов грамматики (все они с пропуском)
GRAMMAR_HINT = "Выбери вариант, который подходит в пропуск"
# Подсказка для вопросов на лексику
LEXIS_HINT = "Выбери слово, которое подходит в пропуск по смыслу"

# Подсказка для заданий True / False / Not stated
TFN_HINT = "Верно (True), неверно (False) или в тексте не сказано (Not stated)?"

QUESTION_RU = {
    # Разговорный / для себя
    "What are Little Free Libraries?": "Что такое Little Free Libraries?",
    "What should you do when you take a book?": "Что нужно сделать, когда берёшь книгу?",
    "Why did Todd Bol build the first one?": "Зачем Тодд Бол построил первую такую библиотеку?",
    "What do many owners say about the boxes?": "Что говорят многие владельцы об этих ящиках?",
    "According to the text, what is multitasking really?": "Чем на самом деле является многозадачность, судя по тексту?",
    "What did studies find about people who often multitask?": "Что исследования выяснили о людях, которые часто делают несколько дел сразу?",
    "Why might the multitasking habit be \"so hard to break\"?": "Почему от привычки делать много дел сразу так трудно избавиться?",
    "What is the writer's overall position?": "Какова общая позиция автора?",
    "Why is Maria calling?": "Зачем звонит Мария?",
    "When does he want to meet?": "Когда он хочет встретиться?",
    "Where will they meet?": "Где они встретятся?",
    "What time will they meet now?": "Во сколько они теперь встретятся?",
    "According to the speaker, what matters most in learning a language?": "Что, по словам говорящего, важнее всего в изучении языка?",
    "What does the speaker think about the idea that language learning depends on talent?":
        "Что говорящий думает об идее, что успех в языке зависит от таланта?",
    "Why do some learners \"freeze\" when someone asks them a question?":
        "Почему некоторые ученики «замирают», когда им задают вопрос?",
    "What does the speaker advise learners to do?": "Что говорящий советует делать ученикам?",

    # ОГЭ
    "The class travelled to Kazan by plane.": "Класс ездил в Казань на самолёте.",
    "Most of the students had visited Kazan before.": "Большинство учеников уже бывали в Казани.",
    "The students tried traditional food in a café.": "Ученики попробовали традиционную еду в кафе.",
    "The trip cost a lot of money.": "Поездка стоила много денег.",
    "According to scientists, why do teenagers find it hard to get up early?":
        "Почему, по мнению учёных, подросткам трудно рано вставать?",
    "When is a typical teenager ready to fall asleep?": "Когда обычный подросток готов заснуть?",
    "What happened in schools that started later?": "Что произошло в школах, где уроки начинались позже?",
    "\"Students' health should come first\" means that...": "Фраза «Students' health should come first» значит, что...",
    "Who is the announcement for?": "Для кого это объявление?",
    "Why will there be no lessons on Friday afternoon?": "Почему в пятницу после обеда не будет уроков?",
    "What should students do before Wednesday if they want to run in the races?":
        "Что нужно сделать до среды тем, кто хочет участвовать в забегах?",
    "Where will the competitions be if it rains?": "Где пройдут соревнования, если будет дождь?",
    "When did Anna start preparing for the exam?": "Когда Анна начала готовиться к экзамену?",
    "What helped Anna's vocabulary most?": "Что больше всего помогло Анне со словарным запасом?",
    "What improved Anna's essay marks?": "Что помогло Анне получать более высокие оценки за сочинения?",
    "What does Anna think about practice tests?": "Что Анна думает о пробных тестах?",

    # ЕГЭ
    "Which heading fits paragraph A?": "Какой заголовок подходит к абзацу A?",
    "Which heading fits paragraph B?": "Какой заголовок подходит к абзацу B?",
    "Which heading fits paragraph C?": "Какой заголовок подходит к абзацу C?",
    "Which heading fits paragraph D?": "Какой заголовок подходит к абзацу D?",
    "What did the experiment show?": "Что показал эксперимент?",
    "According to the researchers, why might boredom lead to creativity?":
        "Почему, по мнению исследователей, скука может вести к творчеству?",
    "The word \"chronic\" in the text is closest in meaning to...": "Слово «chronic» в тексте ближе всего по значению к...",
    "What is the writer's main point?": "Какая главная мысль автора?",
    "Kate has been to Costa Rica before.": "Кейт уже бывала в Коста-Рике.",
    "Kate is going to work with animals in Costa Rica.": "Кейт собирается работать с животными в Коста-Рике.",
    "Volunteers have to pay for their accommodation.": "Волонтёры должны платить за жильё.",
    "Kate's parents supported her plan from the very beginning.": "Родители Кейт с самого начала поддержали её план.",
    "Why did Daniel first become interested in languages?": "Почему Дэниел впервые заинтересовался языками?",
    "How has Daniel's work changed?": "Как изменилась работа Дэниела?",
    "What is Daniel's attitude to machine translation?": "Как Дэниел относится к машинному переводу?",
    "What is Daniel's main advice to young people?": "Какой главный совет Дэниел даёт молодым людям?",

    # Путешествия
    "How far is the hotel from the beach?": "Как далеко отель от пляжа?",
    "What is included in the price?": "Что входит в стоимость?",
    "What can guests do if they arrive before 2 p.m.?": "Что могут сделать гости, если приедут раньше 14:00?",
    "Which of these is true?": "Что из этого верно?",
    "What problem do Venice, Barcelona and Amsterdam share?": "Какая общая проблема у Венеции, Барселоны и Амстердама?",
    "How has overtourism affected local residents?": "Как наплыв туристов повлиял на местных жителей?",
    "What do critics say about measures like entry fees?": "Что критики говорят о мерах вроде платы за вход?",
    "What is the writer's conclusion?": "Какой вывод делает автор?",
    "Where is the flight going?": "Куда летит самолёт?",
    "Why is the flight delayed?": "Почему рейс задерживается?",
    "What is the new departure time?": "Какое новое время вылета?",
    "Where will boarding take place?": "Где будет посадка?",
    "What was the problem with the speaker's early trips?": "В чём была проблема первых поездок говорящей?",
    "How does the speaker travel now?": "Как говорящая путешествует теперь?",
    "What are the benefits of living like a local, according to her?":
        "Какие плюсы, по её словам, у жизни «как местный»?",
    "What does the speaker suggest about museums?": "Что говорящая советует насчёт музеев?",

    # Работа
    "Why should the team come in early on Monday?": "Почему в понедельник команде нужно прийти пораньше?",
    "What time should people arrive on Monday?": "Во сколько нужно прийти в понедельник?",
    "What does Mark say about lunch?": "Что Марк говорит про обед?",
    "Why will the office close early on Friday?": "Почему в пятницу офис закроется раньше?",
    "What did many people predict during the pandemic?": "Что многие предсказывали во время пандемии?",
    "What do surveys show about employees?": "Что опросы показывают о сотрудниках?",
    "Why have some companies called staff back to the office?": "Почему некоторые компании вернули сотрудников в офис?",
    "What does the writer say about the hybrid model?": "Что автор говорит о гибридном формате работы?",
    "Why is David calling?": "Зачем звонит Дэвид?",
    "Why can't he meet on Tuesday morning?": "Почему он не может встретиться во вторник утром?",
    "What does Tom offer to do?": "Что Том предлагает сделать?",
    "What should you do if Wednesday isn't convenient?": "Что нужно сделать, если среда неудобна?",
    "What mistake do new managers often make?": "Какую ошибку часто совершают новые руководители?",
    "What happens when a manager solves every problem?": "Что происходит, когда руководитель сам решает каждую проблему?",
    "How does the speaker feel about asking questions at first?": "Как говорящий сначала относился к тому, чтобы задавать вопросы?",
    "What is the long-term benefit of this approach?": "В чём долгосрочная польза такого подхода?",

    # Для ребёнка
    "Where do the friends sit at school?": "Где друзья сидят в школе?",
    "What does Sofia look like?": "Как выглядит София?",
    "What pets does Sofia have?": "Какие питомцы есть у Софии?",
    "What can the parrot do?": "Что умеет попугай?",
    "Why did William have to leave school?": "Почему Уильяму пришлось бросить школу?",
    "How did William learn to build a windmill?": "Как Уильям научился строить ветряную мельницу?",
    "How did the neighbours' attitude change?": "Как изменилось отношение соседей?",
    "What does William's story show?": "Что показывает история Уильяма?",
    "How old is Max?": "Сколько лет Максу?",
    "What is Max scared of?": "Чего боится Макс?",
    "Where does Max usually sleep?": "Где обычно спит Макс?",
    "When does Ben walk Max?": "Когда Бен гуляет с Максом?",
    "What did the girls want to find out?": "Что хотели выяснить девочки?",
    "Why did they give all the plants the same water and light?":
        "Зачем они давали всем растениям одинаково воды и света?",
    "What was the result?": "Какой получился результат?",
    "What did the teacher think about the result?": "Что учитель подумал о результате?",

    # Бонусный блок C1 (общий для всех целей)
    "What is the \"illusion of explanatory depth\"?": "Что такое «иллюзия глубины понимания»?",
    "What does the speaker find most striking?": "Что больше всего поражает говорящего?",
    "Why did people's views on the policy become more moderate?":
        "Почему взгляды людей на эту политику стали более умеренными?",
    "What is the speaker's attitude to these findings?": "Как говорящий относится к этим результатам?",
    "\"It has become something of a truism\" suggests that the idea is...":
        "Фраза «It has become something of a truism» значит, что эта мысль...",
    "Why do difficult books and music compete \"at a disadvantage\"?":
        "Почему сложные книги и музыка конкурируют «в невыгодном положении»?",
    "What does the writer see as the real danger?": "В чём автор видит настоящую опасность?",
    "Which statement best reflects the writer's view?": "Какое утверждение лучше всего передаёт позицию автора?",
}
