from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_to_menu_markup(texts):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(texts['to_menu'], callback_data='to_menu')
    markup.add(button)
    return markup
