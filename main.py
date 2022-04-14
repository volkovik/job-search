import logging.config
import os

import aiohttp
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery

from data import db_session
from data.users import User
from hhru import HHRU

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
SUPERJOB_TOKEN = os.environ.get("SUPERJOB_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_session.global_init("db/database.db")  # запускаем database

logging.basicConfig(level=logging.INFO)

hh = HHRU()


class WorkForm(StatesGroup):
    profession = State()


@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    await message.reply(
        "Тебя приветсвует бот для поиска работы молодым профессионалам.\n"
        "Давай настроем поиск вакансий под тебя."
    )
    # создаем нового пользователя
    db_sess = db_session.create_session()

    if not db_sess.query(User).filter(User.telegram_id == message.chat.id).first():
        user = User()
        user.telegram_id = message.chat.id

        db_sess.add(user)
        db_sess.commit()

    await WorkForm.profession.set()
    await bot.send_message(message.chat.id, "Напишите какую работы вы хотите:")


@dp.message_handler(state=WorkForm.profession)
async def process_profession(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["profession"] = message.text

    # добавляем специализацию пользователю
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.telegram_id == message.chat.id).first()
    user.specialization = message.text
    db_sess.commit()

    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton("/search"))

    await state.finish()
    await message.reply("Настройка закончена. Давайте начнём поиск работы.", reply_markup=keyboard)


@dp.message_handler(commands=["search"])
async def search_vacancy(message: Message):
    session = db_session.create_session()

    user = session.query(User).filter(User.telegram_id == message.chat.id).first()

    job = await hh.getPage(user.specialization, user.count)
    user.count += 1
    session.commit()

    try:
        await message.reply(
            f"- {hh.parse_name(job)}\n"
            f"- {hh.parse_salary(job)}\n"
            f"Трудовые обязательства: {hh.parse_responsibilities(job)}\n"
            f"Требования: {hh.parse_requirements(job)}\n"
            f"Ссылка: {hh.parse_url(job)}"
        )
    except IndexError:
        await message.reply("По вашей профориентации не было найдено ваканский. Поменяйте профориентацию"
                            "с помощью команды /start")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
