import asyncio
import csv
import html
import logging
import os
import random
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    BufferedInputFile,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import config
from formats import (BUY_NAMES, BUY_TEXT, PRICES, QUIZ, QUIZ_CANDIDATES, QUIZ_RESULT_TEXT, QUIZ_SHORT,
                     QUIZ_WEIGHTS, SECTIONS)
from pdf_report import build_pdf
from price_image import price_png
from question_ru import GRAMMAR_HINT, LEXIS_HINT, QUESTION_RU, TFN_HINT
from questions import (LEVELS, PASS_SCORE, PER_LEVEL, RESULTS, final_level, grammar_level, skill_level,
                       use_hard_tasks)
from tracks import TRACKS

LEADS_FILE = Path(__file__).with_name("leads.csv")
dp = Dispatcher()


class Test(StatesGroup):
    goal = State()
    question = State()
    done = State()
    name = State()
    contact = State()


def kb(rows):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t, callback_data=d)] for t, d in rows]
    )


def result_kb(level: str = ""):
    rows = [("🎁 Записаться на бесплатный урок", "book")]
    if level in ("A0", "A1"):  # начинающим сразу предлагаем курс с нуля
        rows.append(("🌱 Курс «Английский с нуля до A2»", "fn:course_zero"))
    rows += [
        ("💰 Форматы занятий и цены", "formats_new"),
        ("🗣️ Speaking Club", "club"),
        ("🔄 Пройти тест заново", "restart"),
    ]
    return kb(rows)


def user_label(user) -> str:
    name = html.escape(user.full_name)
    return f"{name} (@{user.username})" if user.username else f"{name} (id {user.id})"


async def notify_admin(bot: Bot, text: str):
    if config.ADMIN_ID:
        try:
            await bot.send_message(config.ADMIN_ID, text)
        except Exception as e:  # бот не должен падать, если уведомление не ушло
            logging.warning("Не удалось отправить уведомление: %s", e)


def save_lead(row: dict):
    rows = []
    if LEADS_FILE.exists():
        with LEADS_FILE.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    rows.append(row)
    fields = list(row.keys())
    for old in rows:  # если в старой таблице были другие колонки, сохраняем их тоже
        fields += [k for k in old if k not in fields]
    with LEADS_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, restval="")
        writer.writeheader()
        writer.writerows(rows)


# ---------- старт и цель ----------

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Test.goal)
    await message.answer(
        config.WELCOME_TEXT.format(name=config.TEACHER_NAME),
        reply_markup=kb([(label, f"goal:{i}") for i, (label, _) in enumerate(config.GOALS)]),
    )


@dp.message(Command("myid"))
async def my_id(message: Message):
    await message.answer(f"Твой ID: <code>{message.from_user.id}</code>")


@dp.message(Command("leads"))
async def leads(message: Message):
    if message.from_user.id != config.ADMIN_ID:
        return
    if not LEADS_FILE.exists():
        await message.answer("Заявок пока нет.")
        return
    await message.answer_document(FSInputFile(LEADS_FILE), caption="Все заявки")


@dp.callback_query(Test.goal, F.data.startswith("goal:"))
async def choose_goal(call: CallbackQuery, state: FSMContext):
    goal, track = config.GOALS[int(call.data.split(":")[1])]
    await state.update_data(goal=goal, track=track, blocks=[["g", "A1"]], bi=0, qi=0, scores={})
    await state.set_state(Test.question)
    await call.message.edit_text(
        f"Цель: <b>{html.escape(goal)}</b>\n\nПоехали! 🚀\n\n"
        "✏️ <b>Часть 1. Грамматика и лексика</b>\n"
        "Вопросы будут постепенно усложняться. Если не знаешь ответ, нажми «🤷🏽‍♀️ Не знаю»: "
        "так результат будет точнее, чем если угадывать."
    )
    await send_question(call.message, state, new_message=True)
    await call.answer()


# ---------- вопросы ----------

MEDIA = Path(__file__).with_name("media")
DONT_KNOW = "🤷🏽‍♀️ Не знаю"


def audio_file(track: str, task: str):
    for ext in ("mp3", "m4a", "ogg", "wav"):
        path = MEDIA / f"{track}_{task}.{ext}"
        if path.exists():
            return path
    return None


def block_questions(track: str, block):
    kind, key = block
    module = TRACKS[track]
    return module.GRAMMAR[key][:PER_LEVEL] if kind == "g" else module.TASKS[key]["questions"]


def is_correct(q, option: str) -> bool:
    if option == "x":
        return False
    return int(option) == q.get("answer", 0)


def grammar_scores(scores: dict) -> dict:
    return {lvl: scores.get(f"g:{lvl}", 0) for lvl in LEVELS}


async def send_task_intro(message: Message, track: str, name: str):
    task = TRACKS[track].TASKS[name]
    await message.answer(task["intro"])
    if task["kind"] == "listening":
        path = audio_file(track, name)
        if path.suffix == ".ogg":
            await message.answer_voice(FSInputFile(path))
        else:
            await message.answer_audio(FSInputFile(path), title="Listening task", performer=config.TEACHER_NAME)
    else:
        await message.answer(task["text"])


async def send_question(message: Message, state: FSMContext, new_message=False):
    data = await state.get_data()
    track, blocks, bi, qi = data["track"], data["blocks"], data["bi"], data["qi"]
    block = blocks[bi]
    questions = block_questions(track, block)
    q = questions[qi]
    order = list(range(len(q["options"])))
    if not q.get("fixed"):
        random.shuffle(order)
    if block[0] == "g":
        number = sum(1 for b in blocks[:bi] if b[0] == "g") * PER_LEVEL + qi + 1
        label = f"✏️ Грамматика и лексика · вопрос {number}"
    else:
        kind = TRACKS[track].TASKS[block[1]]["kind"]
        label = ("🎧 Аудирование" if kind == "listening" else "📖 Чтение") + f" · вопрос {qi + 1} из {len(questions)}"
    text = f"{label}\n\n<b>{html.escape(q['text'])}</b>"
    if block[0] == "g":
        hint = LEXIS_HINT if q.get("lexis") else GRAMMAR_HINT
    else:
        hint = QUESTION_RU.get(q["text"], "")
        if q["options"][:3] == ["True", "False", "Not stated"]:
            hint = (hint + "\n" if hint else "") + TFN_HINT
    if hint:
        text += f"\n<i>{html.escape(hint)}</i>"
    rows = [(q["options"][o], f"a:{bi}:{qi}:{o}") for o in order] + [(DONT_KNOW, f"a:{bi}:{qi}:x")]
    if new_message:
        await message.answer(text, reply_markup=kb(rows))
    else:
        await message.edit_text(text, reply_markup=kb(rows))


def plan_next_blocks(data: dict) -> list:
    """После каждого блока решаем, что показывать дальше (тест подстраивается под ученика)."""
    track, blocks, bi, scores = data["track"], data["blocks"], data["bi"], data["scores"]
    kind, key = blocks[bi]
    extra = []
    if kind == "g":
        if scores.get(f"g:{key}", 0) >= PASS_SCORE and key != LEVELS[-1]:
            extra = [["g", LEVELS[LEVELS.index(key) + 1]]]
        else:  # грамматика закончена: одно аудио и один текст под уровень грамматики
            level = "hard" if use_hard_tasks(grammar_level(grammar_scores(scores))) else "easy"
            if audio_file(track, f"listen_{level}"):
                extra.append(["t", f"listen_{level}"])
            extra.append(["t", f"read_{level}"])
    return blocks[:bi + 1] + extra + blocks[bi + 1:]


@dp.callback_query(Test.question, F.data.startswith("a:"))
async def answer(call: CallbackQuery, state: FSMContext):
    _, bi, qi, option = call.data.split(":")
    bi, qi = int(bi), int(qi)
    data = await state.get_data()
    if (bi, qi) != (data["bi"], data["qi"]):  # повторное нажатие на старый вопрос
        await call.answer()
        return

    track, blocks, scores = data["track"], data["blocks"], data["scores"]
    kind, key = blocks[bi]
    questions = block_questions(track, blocks[bi])
    if is_correct(questions[qi], option):
        scores[f"{kind}:{key}"] = scores.get(f"{kind}:{key}", 0) + 1
    await state.update_data(scores=scores)

    if qi + 1 < len(questions):
        await state.update_data(qi=qi + 1)
        await send_question(call.message, state)
        await call.answer()
        return

    # блок закончен
    data = await state.get_data()
    blocks = plan_next_blocks(data)
    bi += 1
    await state.update_data(blocks=blocks, bi=bi, qi=0)
    if bi == len(blocks):
        await call.message.edit_reply_markup(reply_markup=None)
        await show_result(call, state)
    elif blocks[bi][0] == "g":  # следующий уровень грамматики, продолжаем в том же сообщении
        await send_question(call.message, state)
    else:
        await call.message.edit_reply_markup(reply_markup=None)
        await send_task_intro(call.message, track, blocks[bi][1])
        await send_question(call.message, state, new_message=True)
    await call.answer()


def skill_result(scores: dict, part: str):
    for level in ("easy", "hard"):
        if f"t:{part}_{level}" in scores:
            return skill_level(scores[f"t:{part}_{level}"], level == "hard")
    return None


async def show_result(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    track, scores, blocks = data["track"], data["scores"], data["blocks"]
    done = {f"{k}:{v}" for k, v in blocks}
    for key in done:  # блок без единого верного ответа тоже должен учитываться
        scores.setdefault(key, 0)

    grammar = grammar_level(grammar_scores(scores))
    parts = {"Грамматика и лексика": grammar}
    if "t:listen_easy" in done or "t:listen_hard" in done:
        parts["Аудирование"] = skill_result(scores, "listen")
    parts["Чтение"] = skill_result(scores, "read")
    tasks = [v for k, v in scores.items() if k.startswith("t:")]
    perfect = all(k.endswith("_hard") for k in scores if k.startswith("t:")) and all(v == 4 for v in tasks)
    level = final_level(list(parts.values()), grammar_scores(scores), perfect)
    title, description = RESULTS[level]
    breakdown = " · ".join(f"{name}: {lvl}" for name, lvl in parts.items())
    code = title.split("(")[-1].rstrip(")")
    overall = f"💡 Общий уровень ориентировочно {code}."
    if len(set(parts.values())) > 1:
        overall += " Отдельные навыки могут быть развиты сильнее других."
    result_text = (
        f"🎉 Твой уровень: <b>{title}</b>!\n\n"
        "📊 <b>Результаты теста:</b>\n"
        + "\n".join(f"• {name}: {lvl}" for name, lvl in parts.items())
        + f"\n\n{overall}\n\n"
        f"<b>Что это значит?</b> ✨\n{description}\n\n"
        + config.RESULT_NEXT_TEXT
    )
    await state.update_data(level=title, level_key=level, score=breakdown, result_text=result_text)
    await state.set_state(Test.done)

    await call.message.answer(result_text, reply_markup=result_kb(level))
    pdf = build_pdf(level, title, description, call.from_user.first_name or "", track, data["goal"], parts)
    await call.message.answer_document(
        BufferedInputFile(pdf, filename=f"Как учить английский - {level if level != 'A0' else 'A1'}.pdf"),
        caption=(f"📄 Твои рекомендации, как учить английский на уровне {title}.\n\n"
                 f"🎁 Промокод <b>{html.escape(config.PROMO_CODE)}</b>: {html.escape(config.PROMO_TEXT)}. "
                 "Назови его при записи."),
    )
    if config.NOTIFY_ON_RESULT:
        await notify_admin(
            call.bot,
            f"ℹ️ Прошёл тест: {user_label(call.from_user)}\n"
            f"Цель: {html.escape(data['goal'])}\n"
            f"Уровень: {title}\n{breakdown}",
        )


# ---------- кнопки после результата ----------

@dp.callback_query(F.data == "restart")
async def restart(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await start(call.message, state)


@dp.callback_query(F.data == "club")
async def club(call: CallbackQuery):
    await call.message.answer(
        config.CLUB_TEXT,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="Открыть Instagram", url=config.INSTAGRAM_URL)
        ]]),
    )
    await call.answer()


# ---------- форматы занятий и цены ----------

def target_data(target: str) -> str:
    """Куда ведёт кнопка из formats.py -> callback_data для Telegram."""
    if target.startswith("price:"):
        return "p:" + target.split(":", 1)[1]
    if target in ("book", "results", "club") or target.startswith("buy:"):
        return target
    if target == "quiz":
        return "q"
    return "f:" + target


def section_kb(buttons):
    return kb([(label, target_data(target)) for label, target in buttons])


async def show_text(call: CallbackQuery, text: str, markup):
    """Меняем текущее сообщение, а если это картинка - присылаем новое."""
    if call.message.text:
        try:
            await call.message.edit_text(text, reply_markup=markup)
            return
        except TelegramBadRequest:
            pass
    await call.message.answer(text, reply_markup=markup)


@dp.message(Command("formats"))
async def formats_command(message: Message):
    sec = SECTIONS["formats"]
    await message.answer(sec["text"], reply_markup=section_kb(sec["buttons"]))


@dp.callback_query(F.data == "formats_new")
async def formats_new(call: CallbackQuery):
    await formats_command(call.message)
    await call.answer()


@dp.callback_query(F.data.startswith("fn:"))
async def open_section_new(call: CallbackQuery):
    """Раздел отдельным сообщением, чтобы не затирать результат теста."""
    sec = SECTIONS.get(call.data[3:])
    if sec:
        await call.message.answer(sec["text"], reply_markup=section_kb(sec["buttons"]))
    await call.answer()


@dp.callback_query(F.data.startswith("f:"))
async def open_section(call: CallbackQuery):
    sec = SECTIONS.get(call.data[2:])
    if sec:
        await show_text(call, sec["text"], section_kb(sec["buttons"]))
    await call.answer()


@dp.callback_query(F.data.startswith("p:"))
async def open_price(call: CallbackQuery):
    key = call.data[2:]
    price = PRICES.get(key)
    if price:
        await call.message.answer_photo(
            BufferedInputFile(price_png(key), filename=f"price_{key}.png"),
            caption=price["caption"],
            reply_markup=section_kb(price["buttons"]),
        )
    await call.answer()


@dp.callback_query(F.data == "results")
async def back_to_results(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("result_text")
    if text:
        await show_text(call, text, result_kb(data.get("level_key", "")))
    else:
        await show_text(call, "Результаты теста не сохранились. Пройди тест ещё раз, это займёт 8-10 минут.",
                        kb([("🔄 Пройти тест", "restart")]))
    await call.answer()


def quiz_titles(key: str) -> str:
    return "🗣️ Speaking Club" if key == "club" else SECTIONS[key]["title"]


def quiz_pick(goal: str, style: str, load: str) -> list:
    candidates = list(QUIZ_CANDIDATES[goal])
    if goal == "speak" and style not in ("self", "selffb"):
        candidates.remove("course_zero")  # курс для самостоятельного изучения
    score = {k: QUIZ_WEIGHTS[style].get(k, 0) + QUIZ_WEIGHTS[load].get(k, 0) for k in candidates}
    return sorted(candidates, key=lambda k: -score[k])[:3]


@dp.callback_query((F.data == "q") | F.data.startswith("q:"))
async def quiz(call: CallbackQuery):
    answers = call.data.split(":")[1:]
    if len(answers) < len(QUIZ):
        question, options = QUIZ[len(answers)]
        prefix = ":".join(["q"] + answers)
        await show_text(call, f"💡 <b>Подбор формата · вопрос {len(answers) + 1} из {len(QUIZ)}</b>\n\n{question}",
                        kb([(label, f"{prefix}:{value}") for label, value in options]))
    else:
        picks = quiz_pick(*answers)
        items = "\n".join(f"{i}. <b>{quiz_titles(k)}</b>: {QUIZ_SHORT[k]}" for i, k in enumerate(picks, 1))
        rows = [(quiz_titles(k), target_data(k)) for k in picks]
        rows += [("📋 Все форматы", "f:formats"), ("🎁 Записаться на бесплатный урок", "book"),
                 ("🔄 Пройти подбор заново", "q")]
        await show_text(call, QUIZ_RESULT_TEXT.format(items=items), kb(rows))
    await call.answer()


# ---------- запись ----------

@dp.callback_query(F.data == "book")
async def book(call: CallbackQuery, state: FSMContext):
    await state.update_data(interest="Бесплатный пробный урок")
    await state.set_state(Test.name)
    await call.message.answer("Отлично! Запишу тебя на бесплатный пробный урок. Как тебя зовут?")
    await call.answer()


@dp.callback_query(F.data.startswith("buy:"))
async def buy(call: CallbackQuery, state: FSMContext):
    product = BUY_NAMES.get(call.data[4:], "курс")
    await state.update_data(interest=product)
    await state.set_state(Test.name)
    await call.message.answer(BUY_TEXT.format(product=product))
    await call.answer()


@dp.message(Test.name, F.text)
async def got_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip()[:100])
    await state.set_state(Test.contact)
    await message.answer(
        "Оставь телефон (кнопка ниже) или напиши удобный контакт, "
        f"и {config.TEACHER_NAME} свяжется с тобой, чтобы подобрать время.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📱 Отправить номер", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


@dp.message(Test.contact)
async def got_contact(message: Message, state: FSMContext):
    if message.contact:
        contact = message.contact.phone_number
    elif message.text:
        contact = message.text.strip()[:200]
    else:
        await message.answer("Пожалуйста, отправь номер кнопкой или напиши контакт текстом.")
        return

    data = await state.get_data()
    user = message.from_user
    save_lead({
        "дата": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "имя": data.get("name", ""),
        "контакт": contact,
        "telegram": f"@{user.username}" if user.username else str(user.id),
        "уровень": data.get("level", ""),
        "баллы": data.get("score", ""),
        "цель": data.get("goal", ""),
        "интерес": data.get("interest", ""),
    })
    await notify_admin(
        message.bot,
        "🔥 <b>Новая заявка!</b>\n\n"
        f"Имя: {html.escape(data.get('name', ''))}\n"
        f"Контакт: {html.escape(contact)}\n"
        f"Telegram: {user_label(user)}\n"
        f"Уровень: {data.get('level', '-')}\n{data.get('score', '')}\n"
        f"Цель: {html.escape(data.get('goal', '-'))}\n"
        f"Интересует: {html.escape(data.get('interest', '-'))}",
    )
    await state.set_state(Test.done)
    await message.answer(
        f"Спасибо! 💛 Заявка отправлена, {config.TEACHER_NAME} скоро напишет тебе.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.callback_query()
async def stale_button(call: CallbackQuery):
    await call.answer("Эта кнопка уже неактивна. Нажми /start, чтобы начать заново.")


@dp.message()
async def fallback(message: Message):
    await message.answer("Чтобы пройти тест уровня английского, нажми /start\n"
                         "Форматы занятий и цены: /formats")


async def main():
    logging.basicConfig(level=logging.INFO)
    if not config.BOT_TOKEN:
        raise SystemExit("Не задан BOT_TOKEN (токен от @BotFather)")
    bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
