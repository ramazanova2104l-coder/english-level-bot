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
from pdf_report import build_pdf
from questions import (LEVELS, PASS_SCORE, RESULTS, final_level, grammar_level, hard_task_allowed,
                       skill_level)
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


def result_kb():
    return kb([
        ("🎁 Записаться на бесплатный урок", "book"),
        ("🗣 Speaking Club", "club"),
        ("🔄 Пройти тест заново", "restart"),
    ])


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
    new_file = not LEADS_FILE.exists()
    with LEADS_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if new_file:
            writer.writeheader()
        writer.writerow(row)


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
        "Вопросы будут постепенно усложняться. Если не знаешь ответ, нажми «🤷 Не знаю»: "
        "так результат будет точнее, чем если угадывать."
    )
    await send_question(call.message, state, new_message=True)
    await call.answer()


# ---------- вопросы ----------

MEDIA = Path(__file__).with_name("media")
DONT_KNOW = "🤷 Не знаю"


def audio_file(track: str, task: str):
    for ext in ("mp3", "m4a", "ogg", "wav"):
        path = MEDIA / f"{track}_{task}.{ext}"
        if path.exists():
            return path
    return None


def block_questions(track: str, block):
    kind, key = block
    module = TRACKS[track]
    return module.GRAMMAR[key] if kind == "g" else module.TASKS[key]["questions"]


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
        number = sum(1 for b in blocks[:bi] if b[0] == "g") * 5 + qi + 1
        label = f"✏️ Грамматика и лексика · вопрос {number}"
    else:
        kind = TRACKS[track].TASKS[block[1]]["kind"]
        label = ("🎧 Аудирование" if kind == "listening" else "📖 Чтение") + f" · вопрос {qi + 1} из {len(questions)}"
    text = f"{label}\n\n<b>{html.escape(q['text'])}</b>"
    rows = [(q["options"][o], f"a:{bi}:{qi}:{o}") for o in order] + [(DONT_KNOW, f"a:{bi}:{qi}:x")]
    if new_message:
        await message.answer(text, reply_markup=kb(rows))
    else:
        await message.edit_text(text, reply_markup=kb(rows))


def plan_next_blocks(data: dict) -> list:
    """После каждого блока решаем, что показывать дальше (тест подстраивается под ученика)."""
    track, blocks, bi, scores = data["track"], data["blocks"], data["bi"], data["scores"]
    kind, key = blocks[bi]
    score = scores.get(f"{kind}:{key}", 0)
    extra = []
    if kind == "g":
        if score >= PASS_SCORE and key != LEVELS[-1]:
            extra = [["g", LEVELS[LEVELS.index(key) + 1]]]
        else:  # грамматика закончена, дальше аудирование и чтение
            if audio_file(track, "listen_easy"):
                extra.append(["t", "listen_easy"])
            extra.append(["t", "read_easy"])
    elif key.endswith("_easy"):
        hard = key.replace("_easy", "_hard")
        grammar = grammar_level(grammar_scores(scores))
        if hard_task_allowed(score, grammar) and (hard.startswith("read") or audio_file(track, hard)):
            extra = [["t", hard]]
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
    if f"t:{part}_easy" not in scores:
        return None
    return skill_level(scores[f"t:{part}_easy"], scores.get(f"t:{part}_hard"))


async def show_result(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    track, scores, blocks = data["track"], data["scores"], data["blocks"]
    done = {f"{k}:{v}" for k, v in blocks}
    for key in done:  # блок без единого верного ответа тоже должен учитываться
        scores.setdefault(key, 0)

    grammar = grammar_level(grammar_scores(scores))
    parts = {"Грамматика и лексика": grammar}
    if "t:listen_easy" in done:
        parts["Аудирование"] = skill_result(scores, "listen")
    parts["Чтение"] = skill_result(scores, "read")
    level = final_level(list(parts.values()), grammar_scores(scores))
    title, description = RESULTS[level]
    breakdown = " · ".join(f"{name}: {lvl}" for name, lvl in parts.items())
    await state.update_data(level=title, score=breakdown)
    await state.set_state(Test.done)

    await call.message.answer(
        f"🎉 Готово!\n\nТвой уровень: <b>{title}</b>\n"
        + "\n".join(f"• {name}: {lvl}" for name, lvl in parts.items())
        + f"\n\n{description}\n\n"
        f"Говорение {config.TEACHER_NAME} проверит на бесплатном пробном уроке "
        "и составит план под твою цель.\n\n"
        + config.LESSON_TEXT.format(name=config.TEACHER_NAME),
        reply_markup=result_kb(),
    )
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


@dp.callback_query(F.data == "book")
async def book(call: CallbackQuery, state: FSMContext):
    await state.set_state(Test.name)
    await call.message.answer("Отлично! Запишу тебя на бесплатный пробный урок. Как тебя зовут?")
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
    })
    await notify_admin(
        message.bot,
        "🔥 <b>Новая заявка на урок!</b>\n\n"
        f"Имя: {html.escape(data.get('name', ''))}\n"
        f"Контакт: {html.escape(contact)}\n"
        f"Telegram: {user_label(user)}\n"
        f"Уровень: {data.get('level', '-')}\n{data.get('score', '')}\n"
        f"Цель: {html.escape(data.get('goal', '-'))}",
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
    await message.answer("Чтобы пройти тест уровня английского, нажми /start")


async def main():
    logging.basicConfig(level=logging.INFO)
    if not config.BOT_TOKEN:
        raise SystemExit("Не задан BOT_TOKEN (токен от @BotFather)")
    bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
