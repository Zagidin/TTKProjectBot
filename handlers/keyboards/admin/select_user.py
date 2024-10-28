from bot.bot import dp
from aiogram.types import Message
from base.config import SessionLocal, Client


@dp.message_handler(text="Вывести Пользователей")
async def all_user(message: Message):
    with SessionLocal() as session:
        clients = session.query(Client).all()

    if not clients:
        await message.answer("Нет зарегистрированных пользователей.")
        return
    else:
        await message.answer("Вот файл со всеми пользователями 🔖")

    response_text = "Список пользователей:\n\n"

    for client in clients:
        response_text += (
            f"{'#' * 90}\n"
            f"🎟 Номер договора: {client.contract}\n"
            f"📞 Контактный номер: {client.phone}\n"
            f"🏡 Адрес: {client.address}\n"
            f"🎫 Услуга: {client.service}\n"
            f"🛒 Цель: {client.intent}\n"
            f"👤 Описание: {client.user_text}\n"
            f"{'-' * 90}\n"
        )

    user_id = message.from_user.id
    file_path = "handlers/keyboards/admin/all_user.txt"

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response_text)

    with open(file_path, 'rb') as file:
        await dp.bot.send_document(chat_id=user_id, document=file)
