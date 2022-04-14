import logging.config
import os

import aiohttp
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery

from utilities import Experience

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
SUPERJOB_TOKEN = os.environ.get("SUPERJOB_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)


class WorkForm(StatesGroup):
    profession = State()


@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    await message.reply(
        "Тебя приветсвует бот для поиска работы молодым профессионалам.\n"
        "Давай настроем поиск вакансий под тебя."
    )

    await WorkForm.profession.set()
    await bot.send_message(message.chat.id, "Какая у тебя профориентация?")


@dp.message_handler(state=WorkForm.profession)
async def process_profession(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["profession"] = message.text

    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton("/search"))

    await state.finish()
    await message.reply("Настройка закончена. Давайте начнём поиск работы.", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
