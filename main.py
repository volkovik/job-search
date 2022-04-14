import logging.config
import os

from aiogram import Bot, Dispatcher, types, executor


TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Hello!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
