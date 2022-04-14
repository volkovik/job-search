import logging.config
import os

import aiohttp
from aiogram import Bot, Dispatcher, types, executor


TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Hello!")


@dp.message_handler(commands=["info"])
async def send_info(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.hh.ru/') as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            print(await response.json())
            html = await response.text()
            print("Body:", html[:15], "...")


    await message.reply("cringe")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
