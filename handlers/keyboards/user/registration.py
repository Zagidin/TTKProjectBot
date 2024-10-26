import os
import pymorphy2
from bot.bot import dp
from random import randint
from pydub import AudioSegment
import speech_recognition as sr
from aiogram.dispatcher import FSMContext
from base.config import SessionLocal, Client
from status_machine.user import UserRegistration
from keyboards.reply_key.user.sign_user import start_keyboard
from aiogram.types import Message, ReplyKeyboardRemove, ContentType


#     # contract_number = "516"
#     # for _ in range(7):
#     #     with SessionLocal() as session:
#     #         exists = session.query(Client).filter(Client.contract == contract_number).first()
#     #         if not exists:
#     #             contract_number += str(randint(0, 9))
#     #
#     # new_client = Client(contract=contract_number, phone=data['phone'],
#     #                     address=data['address'], service=data['service'])
#     #
#     # with SessionLocal() as session:
#     #     session.add(new_client)
#     #     session.commit()
#     #
#     # await message.answer(
#     #     text="Данные успешно переданы ✅"
#     #          "\nCкоро с Вами свяжутся специалисты 🤳",
#     #     reply_markup=start_keyboard
#     # )

my_list_str = {
    "тариф": ["изменение тарифа", "поменять тариф", "сменить тариф", "изменить тариф", "смена тарифа"],
    "услуга": ["подключить услугу", "подключение услуги", "добавить услугу", "добавление услуги", "услуга"],
    "договор": ["заключить договор", "оформить договор", "договор", "расторгнуть договор"]
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
    with open("gs_user/user_gs_start.ogg", "wb") as new_file:
        new_file.write(downloaded_file.getvalue())

    # Проверяем наличие ffmpeg
    if not os.system("ffmpeg -version >nul 2>nul"):
        recognizer = sr.Recognizer()

        # Конвертируем OGG в WAV
        audio = AudioSegment.from_ogg("gs_user/user_gs_start.ogg")
        audio.export("gs_user/user_gs_finish.wav", format="wav")

        with sr.AudioFile("gs_user/user_gs_finish.wav") as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="ru-RU")
                print(type(text))

                # Лемматизация текста
                lemmatized_text = ' '.join([morph.parse(word)[0].normal_form for word in text.split()])

                # Проверяем наличие слов из списка в распознанном тексте
                found_keys = []
                for key, phrases in my_list_str.items():
                    if any(phrase in lemmatized_text for phrase in phrases):
                        found_keys.append(key)

                if found_keys:
                    await message.answer(
                        f"Найдены следующие категории: {', '.join(found_keys)}\n\nТекст: {lemmatized_text}")
                else:
                    await message.answer(f"Ни одно из слов не найдено ({my_list_str})\n\nТекст: {lemmatized_text}")
            except sr.UnknownValueError:
                await message.answer("Не удалось распознать речь.")
            except sr.RequestError as e:
                await message.answer(f"Ошибка сервиса: {e}")
    else:
        await message.answer("FFmpeg не найден. Пожалуйста, установите FFmpeg.")

    await state.finish()