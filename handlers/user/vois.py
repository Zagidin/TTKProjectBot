import os
from bot.bot import dp
from aiogram import types
from aiogram.types import Message
from pydub import AudioSegment
import speech_recognition as sr

my_list_str = ["тариф", "услуги", "войти", "зарегистрироваться"]


@dp.message_handler(commands=['vois'])
async def vois(msg: Message):
    await msg.answer(text="Введите голосовое сообщение...")


@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_voice(message: Message):
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

                # Проверяем наличие слов из списка в распознанном тексте
                found_words = [slovo for slovo in my_list_str if slovo in text]

                if found_words:
                    await message.answer(f"Найдены следующие слова: {', '.join(found_words)}\n\nТекст: {text}")
                else:
                    await message.answer(f"Ни одно из слов не найдено ({my_list_str})\n\nТекст: {text}")
            except sr.UnknownValueError:
                await message.answer("Не удалось распознать речь.")
            except sr.RequestError as e:
                await message.answer(f"Ошибка сервиса: {e}")
    else:
        await message.answer("FFmpeg не найден. Пожалуйста, установите FFmpeg.")

# --------------------------------------------------------------------------------------
# import os
#
# from bot.bot import dp
# from aiogram import types
# from aiogram.types import Message
# from pydub import AudioSegment
# import speech_recognition as sr
#
# my_list_str = ["тариф", "услуги", "войти", "зарегистрироваться"]
#
#
# @dp.message_handler(commands=['vois'])
# async def vois(msg: Message):
#     await msg.answer(
#         text="Введите голосовое сообщение..."
#     )
#
#
# @dp.message_handler(content_types=types.ContentType.VOICE)
# async def handle_voice(message: Message):
#     file_id = message.voice.file_id
#     file_info = await dp.bot.get_file(file_id)
#
#     downloaded_file = await dp.bot.download_file(file_info.file_path)
#
#     # Сохраняем файл во временное хранилище
#     with open("voice_message.ogg", "wb") as new_file:
#         new_file.write(downloaded_file.getvalue())
#
#     # Проверяем наличие ffmpeg
#     if not os.system("ffmpeg -version >nul 2>nul"):
#         recognizer = sr.Recognizer()
#
#         # Конвертируем OGG в WAV
#         audio = AudioSegment.from_ogg("voice_message.ogg")
#         audio.export("voice_message.wav", format="wav")
#
#         with sr.AudioFile("voice_message.wav") as source:
#             audio_data = recognizer.record(source)
#
#             try:
#                 text = recognizer.recognize_google(audio_data, language="ru-RU")
#                 print(type(text))
#
#                 # Проверяем наличие слов
#                 found_words = [slovo for slovo in my_list_str if slovo in text]
#
#                 if found_words:
#                     await message.answer(f"Ура! Вы сказали: {text}")
#                 else:
#                     await message.answer(f"Крутых слов нет ({my_list_str})\n\n{text}")
#
#             except sr.UnknownValueError:
#                 await message.answer("Не удалось распознать речь.")
#             except sr.RequestError as e:
#                 await message.answer(f"Ошибка сервиса: {e}")
#     else:
#         await message.answer("FFmpeg не найден. Пожалуйста, установите FFmpeg.")
