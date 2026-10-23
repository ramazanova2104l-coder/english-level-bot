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
from questions import LEVELS, LISTENING, QUESTIONS, READING, RESULTS, calc_level

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
        reply_markup=kb([(g, f"goal:{i}") for i, g in enumerate(config.GOALS)]),
    )


@dp.message(Command("myid"))
async def my_id(message: Message):
    await message.answer(f"Ваш ID: <code>{message.from_user.id}</code>")


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
    goal = config.GOALS[int(call.data.split(":")[1])]
    await state.update_data(goal=goal, step=0, steps=build_steps(),
                            correct={lvl: 0 for lvl in LEVELS})
    await state.set_state(Test.question)
    await call.message.edit_text(f"Цель: <b>{html.escape(goal)}</b>\n\nПоехали! 🚀\n\n✏️ <b>Грамматика</b>")
    await send_question(call.message, state, new_message=True)
    await call.answer()


# ---------- вопросы ----------

SECTIONS = {"grammar": QUESTIONS, "listening": LISTENING["questions"], "reading": READING["questions"]}
SECTION_LABELS = {"grammar": "✏️ Грамматика", "listening": "🎧 Аудирование", "reading": "📖 Чтение"}
MEDIA = Path(__file__).with_name("media")


def listening_file():
    for ext in ("mp3", "m4a", "ogg", "wav"):
        path = MEDIA / f"listening.{ext}"
        if path.exists():
            return path
    return None


def build_steps():
    """Порядок вопросов: грамматика, аудио (если есть запись), текст."""
    sections = ["grammar"] + (["listening"] if listening_file() else []) + ["reading"]
    return [[section, i] for section in sections for i in range(len(SECTIONS[section]))]


def question_of(step):
    section, i = step
    return SECTIONS[section][i]


async def send_section_intro(message: Message, section: str):
    if section == "listening":
        await message.answer(LISTENING["intro"])
        path = listening_file()
        if path.suffix == ".ogg":
            await message.answer_voice(FSInputFile(path))
        else:
            await message.answer_audio(FSInputFile(path), title="Listening task", performer=config.TEACHER_NAME)
    elif section == "reading":
        await message.answer(READING["intro"])
        await message.answer(READING["text"])


async def send_question(message: Message, state: FSMContext, new_message=False):
    data = await state.get_data()
    steps, step = data["steps"], data["step"]
    section = steps[step][0]
    q = question_of(steps[step])
    order = list(range(len(q["options"])))
    random.shuffle(order)
    text = (f"{SECTION_LABELS[section]} · вопрос {step + 1} из {len(steps)}\n\n"
            f"<b>{html.escape(q['text'])}</b>")
    markup = kb([(q["options"][o], f"ans:{step}:{o}") for o in order])
    if new_message:
        await message.answer(text, reply_markup=markup)
    else:
        await message.edit_text(text, reply_markup=markup)


@dp.callback_query(Test.question, F.data.startswith("ans:"))
async def answer(call: CallbackQuery, state: FSMContext):
    _, step, option = call.data.split(":")
    step, option = int(step), int(option)
    data = await state.get_data()
    if step != data["step"]:  # повторное нажатие на старый вопрос
        await call.answer()
        return

    steps, correct = data["steps"], data["correct"]
    q = question_of(steps[step])
    if option == 0:  # правильный ответ в questions.py всегда первый
        correct[q["level"]] += 1
    step += 1
    await state.update_data(step=step, correct=correct)

    if step == len(steps):
        await call.message.edit_reply_markup(reply_markup=None)
        await show_result(call, state)
    elif steps[step][0] != steps[step - 1][0]:  # начинается новый блок
        await call.message.edit_reply_markup(reply_markup=None)
        await send_section_intro(call.message, steps[step][0])
        await send_question(call.message, state, new_message=True)
    else:
        await send_question(call.message, state)
    await call.answer()


async def show_result(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    steps = data["steps"]
    asked = {lvl: 0 for lvl in LEVELS}
    for st in steps:
        asked[question_of(st)["level"]] += 1
    level = calc_level(data["correct"], asked)
    score = sum(data["correct"].values())
    title, description = RESULTS[level]
    await state.update_data(level=title, score=f"{score}/{len(steps)}")
    await state.set_state(Test.done)

    await call.message.answer(
        f"🎉 Готово! Правильных ответов: {score} из {len(steps)}\n\n"
        f"Ваш уровень: <b>{title}</b>\n\n{description}\n\n"
        f"Говорение {config.TEACHER_NAME} проверит на бесплатном пробном уроке "
        "и составит план под вашу цель.\n\n"
        + config.LESSON_TEXT.format(name=config.TEACHER_NAME),
        reply_markup=result_kb(),
    )
    pdf = build_pdf(level, title, description, call.from_user.first_name or "")
    await call.message.answer_document(
        BufferedInputFile(pdf, filename=f"Как учить английский — {level if level != 'A0' else 'A1'}.pdf"),
        caption=(f"📄 Ваши рекомендации, как учить английский на уровне {title}.\n\n"
                 f"🎁 Промокод <b>{html.escape(config.PROMO_CODE)}</b>: {html.escape(config.PROMO_TEXT)}. "
                 "Назовите его при записи."),
    )
    if config.NOTIFY_ON_RESULT:
        await notify_admin(
            call.bot,
            f"ℹ️ Прошёл тест: {user_label(call.from_user)}\n"
            f"Уровень: {title} ({score}/{len(steps)})\n"
            f"Цель: {html.escape(data['goal'])}",
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
    await call.message.answer("Отлично! Запишу вас на бесплатный пробный урок. Как вас зовут?")
    await call.answer()


@dp.message(Test.name, F.text)
async def got_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip()[:100])
    await state.set_state(Test.contact)
    await message.answer(
        "Оставьте телефон (кнопка ниже) или напишите удобный контакт, "
        f"и {config.TEACHER_NAME} свяжется с вами, чтобы подобрать время.",
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
        await message.answer("Пожалуйста, отправьте номер кнопкой или напишите контакт текстом.")
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
        f"Уровень: {data.get('level', '—')} ({data.get('score', '—')})\n"
        f"Цель: {html.escape(data.get('goal', '—'))}",
    )
    await state.set_state(Test.done)
    await message.answer(
        f"Спасибо! 💛 Заявка отправлена, {config.TEACHER_NAME} скоро напишет вам.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.callback_query()
async def stale_button(call: CallbackQuery):
    await call.answer("Эта кнопка уже неактивна. Нажмите /start, чтобы начать заново.")


@dp.message()
async def fallback(message: Message):
    await message.answer("Чтобы пройти тест уровня английского, нажмите /start")


async def main():
    logging.basicConfig(level=logging.INFO)
    if not config.BOT_TOKEN:
        raise SystemExit("Не задан BOT_TOKEN (токен от @BotFather)")
    bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
