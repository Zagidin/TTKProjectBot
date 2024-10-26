from bot.bot import dp
from aiogram.types import Message, ContentType


@dp.message_handler(text="Изменить Триггеры (ключевые слова)")
async def edit_file(message: Message):
    user_id = message.from_user.id
    file_path = 'handlers/keyboards/admin/admin_trigger_settings.txt'

    await message.answer("Файл успешно отправлен 🎉\nОтредактируйте файл и отправьте заново.")

    with open(file_path, 'rb') as file:
        await dp.bot.send_document(chat_id=user_id, document=file)


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def download_file(message: Message):
    file_id = message.document.file_id

    file_info = await dp.bot.get_file(file_id)
    file_path = file_info.file_path

    custom_file_name = "admin_trigger_settings.txt"
    download_path = f"handlers/keyboards/admin/{custom_file_name}"

    await dp.bot.download_file(file_path, download_path)

    await message.answer("Файл успешно скачан!")
