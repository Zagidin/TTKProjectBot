from bot.bot import dp
from aiogram.utils import executor


def start_bot():
    print('Бот запущен!\nВсе обновления пропущена: ', end=' ')
    executor.start_polling(dp, skip_updates=True)
    print("Бот остановлен!")
