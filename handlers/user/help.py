from bot.bot import dp
from aiogram.types import Message


@dp.message_handler(commands=['help'])
async def help_bot(message: Message):
    await message.answer(
        text=f"Привет @{message.from_user.username} 👋\n"
             f"Чтобы зарегеться Вам нужно /start\n"
             f"И выбрать из меню кнопок и Заключить новый договор 🎆\n\n<i>Дальше в разработке ...</i>",
        parse_mode='HTML'
    )
