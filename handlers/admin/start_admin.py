from os import getenv
from bot.bot import dp
from dotenv import load_dotenv
from aiogram.types import Message


@dp.message_handler(commands='admin')
async def admin(message: Message):
    await message.answer(
        text="Введите Логин администратора"
    )