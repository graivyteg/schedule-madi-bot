from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_even_odd_markup(texts) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    t = texts['even_odd_markup']
    btn1 = InlineKeyboardButton(t['odd'], callback_data='get_odd_week')
    btn2 = InlineKeyboardButton(t['even'], callback_data='get_even_week')
    btn3 = InlineKeyboardButton(t['any'], callback_data='get_all_week')
    btn4 = InlineKeyboardButton(texts['to_menu'], callback_data='to_menu')
    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    keyboard.add(btn4)
    return keyboard