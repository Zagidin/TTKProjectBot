from aiogram.dispatcher.filters.state import State, StatesGroup


class Admin(StatesGroup):
    login = State()
    password = State()
