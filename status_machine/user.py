from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    action = State()
    enter_contract_number = State()
    enter_contact_info = State()
