from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = KeyboardButton(text="Добавить Администратора")
btn2 = KeyboardButton(text="Добавить Редактора")
btn3 = KeyboardButton(text="Вывести Пользователей")
btn4 = KeyboardButton(text="Изменить Триггеры (ключевые слова)")
start_admin_panel.row(btn1, btn2)
start_admin_panel.add(btn3)
start_admin_panel.add(btn4)
