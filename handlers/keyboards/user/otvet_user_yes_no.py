# from bot.bot import dp
# from random import randint
# from aiogram.types import Message
# from base.config import SessionLocal, Client
# from keyboards.reply_key.user.sign_user import start_keyboard
#
#
#
# @dp.message_handler(text="Да")
# async def yes_user_otvet(message: Message):
#     await message.answer(
#             text="Данные успешно переданы ✅"
#                  "\nCкоро с Вами свяжутся специалисты 🤳",
#             reply_markup=start_keyboard
#         )
#
#     contract_number = "516"
#         for _ in range(7):
#             with SessionLocal() as session:
#                 exists = session.query(Client).filter(Client.contract == contract_number).first()
#                 if not exists:
#                     contract_number += str(randint(0, 9))
#
#         new_client = Client(contract=contract_number, phone=data['phone'],
#                             address=data['address'], service=data['service'])
#
#         with SessionLocal() as session:
#             session.add(new_client)
#             session.commit()
#
#
#
# @dp.message_handler(text="Нет")
# async def yes_user_otvet(message: Message):
#     await message.answer(
#             text="Пожалуйста, Если возникла проблема, напишите текстовое сообщение, которое отправится администратору",
#             reply_markup=start_keyboard
#         )