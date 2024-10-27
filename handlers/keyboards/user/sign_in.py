from bot.bot import dp
from aiogram.types import Message
from status_machine.user import User
from aiogram.dispatcher import FSMContext
from base.config import SessionLocal, Client
from keyboards.reply_key.user.sign_user import start_keyboard


@dp.message_handler(text="Войти как клиент ТТК")
async def sign_user(message: Message):
    await message.answer(
        text="✍ Введите Ваш номер Договора:"
    )
    await User.contract.set()


@dp.message_handler(state=User.contract)
async def contract_input(message: Message, state: FSMContext):

    async with state.proxy() as data:
        data['contract'] = message.text

    await state.finish()

    contract_number = message.text

    if contract_number:
        with SessionLocal() as session:
            client = session.query(Client).filter(Client.contract == contract_number).first()
            if client:
                await message.answer(
                    f"Добро пожаловать!\n"
                    f"Ваш контактный номер: {client.phone}, "
                    f"адрес: {client.address}."
                )
                await message.answer(
                    text="\n"
                         "<b>Предлагаемые нами тарифы и услуги:\n</b>"
                         "\n<b>Список тарифов:\n</b>"
                         "\tМаксимальный - 1000 Гбит 800р в месяц\n"
                         "\tМощный - 100 Мбит 400р в месяц\n"
                         "\tЧестный - 10 Мбит 100р в месяц\n"
                         "\n\n<b>Список услуг:</b>\n"
                         "\tАнтиВирус Касперский - 100р в месяц\n"
                         "\tВыделенный IP - 100р в месяц\n"
                         "\tПерсональный менеджер - 100р в месяц\n"
                         "\tФирменный роутер - 100р в месяц\n"
                         "\n\n\n<i>И другой функционал</i>",
                    parse_mode="HTML"
                )
            else:
                await message.answer(
                    text="Номер договора не найден.\nПопробуйте войти ещё раз!",
                    reply_markup=start_keyboard
                )
    else:
        await message.answer(
            text="Неверный формат номера договора.\nВведите свой номер договора выданный администратором 🎫",
            reply_markup=start_keyboard
        )