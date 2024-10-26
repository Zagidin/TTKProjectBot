import os
import pymorphy2
from bot.bot import dp
from pydub import AudioSegment
import speech_recognition as sr
from aiogram.dispatcher import FSMContext
from status_machine.user import UserRegistration
from aiogram.types import Message, ReplyKeyboardRemove, ContentType


my_list_str = {
    "тарифы": {
        "триггеры": ["максимальный", "мощный", "честный", "изменение тарифа", "тариф", "сменить тариф", "смена тарифа"],
        "описание": "Запрос информации или изменения тарифного плана."
    },
    "услуги": {
        "триггеры": ["антивирус", "касперский", "выделенный ip", "ip", "IP", "персональный менеджер", "менеджер",
                     "фирменный роутер", "роутер", "подключить услугу", "услуга", "добавить услугу"],
        "описание": "Запрос подключения или информации по дополнительным услугам."
    },
    "договор": {
        "триггеры": ["заключить договор", "оформить договор", "расторгнуть договор", "договор"],
        "описание": "Запрос на заключение, расторжение или изменение договора."
    }
}

morph = pymorphy2.MorphAnalyzer()

@dp.message_handler(text="Заключить новый договор")
async def registration_user(message: Message):
    await message.answer(
        text="Укажите Ваш номер телефона ☎",
        reply_markup=ReplyKeyboardRemove()
    )
    await UserRegistration.phone.set()

@dp.message_handler(state=UserRegistration.phone)
async def user_phone(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    await message.reply(
        text="Теперь введите Ваш адрес, для получения услуги ✨",
        reply_markup=ReplyKeyboardRemove()
    )
    await UserRegistration.next()

@dp.message_handler(state=UserRegistration.address)
async def user_address(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text

    await message.answer(
        text="<b>Предлагаемые нами тарифы и услуги:\n</b>"
             "\n<b>Список тарифов:\n</b>"
             "\tМаксимальный - 1000 Гбит 800р в месяц\n"
             "\tМощный - 100 Мбит 400р в месяц\n"
             "\tЧестный - 10 Мбит 100р в месяц\n"
             "\n\n<b>Список услуг:</b>\n"
             "\tАнтиВирус Касперский - 100р в месяц\n"
             "\tВыделенный IP - 100р в месяц\n"
             "\tПерсональный менеджер - 100р в месяц\n"
             "\tФирменный роутер - 100р в месяц\n",
        parse_mode="HTML"
    )

    await message.answer(
        text="Выбрав интересующие вас опции из нашего списка продуктов."
             "\nСообщите нам об этом с помощью текстового или голосового сообщения..."
    )

    await UserRegistration.next()

@dp.message_handler(content_types=ContentType.VOICE, state=UserRegistration.service)
async def user_provider_service(message: Message, state: FSMContext):
    file_id = message.voice.file_id
    file_info = await dp.bot.get_file(file_id)
    downloaded_file = await dp.bot.download_file(file_info.file_path)

    # Сохраняем файл во временное хранилище
    with open("sound_user/user_gs_start.ogg", "wb") as new_file:
        new_file.write(downloaded_file.getvalue())

    # Проверяем наличие ffmpeg
    if not os.system("ffmpeg -version >nul 2>nul"):
        recognizer = sr.Recognizer()

        # Конвертируем OGG в WAV
        audio = AudioSegment.from_ogg("sound_user/user_gs_start.ogg")
        audio.export("sound_user/user_gs_finish.wav", format="wav")

        with sr.AudioFile("sound_user/user_gs_finish.wav") as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="ru-RU")

                # Лемматизация текста
                lemmatized_text = ' '.join([morph.parse(word)[0].normal_form for word in text.split()])

                # Проверяем наличие триггеров и выводим описание
                found_descriptions = []
                for key, value in my_list_str.items():
                    if any(trigger in lemmatized_text for trigger in value["триггеры"]):
                        found_descriptions.append(f"{value['описание']}")

                if found_descriptions:
                    await message.answer(
                        text="Правильно ли я Вас понял?\nСреди ваших запросов есть: "
                    )
                    await message.answer("\t" + "\n".join(found_descriptions))
                else:
                    await message.answer(f"К сожалению я Вас не понял, попробуйте повторно "
                                         f"записать голосовое сообщение или напишите текстом 😟")
            except sr.UnknownValueError:
                await message.answer("Не удалось распознать речь.")
            except sr.RequestError as e:
                await message.answer(f"Ошибка сервиса: {e}")
    else:
        await message.answer("FFmpeg не найден. Пожалуйста, установите FFmpeg.")

    await state.finish()
