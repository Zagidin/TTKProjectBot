import re
from bot.bot import dp
from random import randint
from aiogram.types import Message
from status_machine.user import User
from aiogram.dispatcher import FSMContext
from keyboards.reply_key.user.start_key import start_keyboard
from base.config import SessionLocal, Client


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer("Выберите действие:", reply_markup=start_keyboard)

    await User.action.set()


@dp.message_handler(state=User.action)
async def process_action(message: Message, state: FSMContext):
    if message.text == "Войти как клиент ТТК":
        await message.answer("Введите номер договора (516xxxxx):")
        await User.enter_contract_number.set()
    elif message.text == "Заключить новый договор":
        await message.answer("Введите ваш контактный номер и адрес для подключения (номер, адрес):")

        await User.enter_contact_info.set()


@dp.message_handler(state=User.enter_contract_number)
async def process_contract_number(message: Message, state: FSMContext):
    contract_number_pattern = r"^516\d{7}$"

    contract_number = message.text.strip()

    if re.match(contract_number_pattern, contract_number):
        with SessionLocal() as session:
            client = session.query(Client).filter(Client.contract_number == contract_number).first()
            if client:
                await message.answer(
                    f"Добро пожаловать! Ваш контактный номер: {client.contact_number}, адрес: {client.address}.")
            else:
                await message.answer("Номер договора не найден.")
        await state.finish()
    else:
        await message.answer("Неверный формат номера договора.")


@dp.message_handler(state=User.enter_contract_number)
async def process_contract_number(message: Message, state: FSMContext):
    contract_number_pattern = r"^516\d{7}$"

    contract_number = message.text.strip()

    if re.match(contract_number_pattern, contract_number):
        with SessionLocal() as session:
            client = session.query(Client).filter(Client.contract_number == contract_number).first()
            if client:
                await message.answer(
                    f"Добро пожаловать! Ваш контактный номер: {client.contact_number}, адрес: {client.address}.")
            else:
                await message.answer("Номер договора не найден.")
        await state.finish()
    else:
        await message.answer("Неверный формат номера договора.")


@dp.message_handler(state=User.enter_contact_info)
async def process_contact_info(message: Message, state: FSMContext):
    contact_info = message.text.split(",")

    if len(contact_info) == 2:
        contact_number = contact_info[0].strip()
        address = contact_info[1].strip()
        contract_number = "516"
        for _ in range(7):
            with SessionLocal() as session:
                exists = session.query(Client).filter(Client.contract_number == contract_number).first()
                if not exists:
                    contract_number += str(randint(0,9))


        new_client = Client(contract_number=contract_number, contact_number=contact_number,
                            address=address)

        with SessionLocal() as session:
            session.add(new_client)
            session.commit()

        await message.answer("Ваши данные сохранены. Спасибо!")
        await state.finish()
    else:
        await message.answer("Пожалуйста, укажите контактный номер и адрес через запятую.")