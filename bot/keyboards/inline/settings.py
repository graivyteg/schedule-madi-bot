from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_settings_markup(texts):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(texts['settings_markup']['change_name'], callback_data='change_name')
    btn2 = InlineKeyboardButton(texts['settings_markup']['change_group'], callback_data='change_group')
    btn3 = InlineKeyboardButton(texts['settings_markup']['help'], callback_data='help')
    btn4 = InlineKeyboardButton(texts['to_menu'], callback_data='to_menu')
    markup.row(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    return markup
