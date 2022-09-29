from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.answers import is_name_right_markup_answers


def get_name_right_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(is_name_right_markup_answers['right'])
    btn2 = KeyboardButton(is_name_right_markup_answers['wrong'])
    markup.add(btn1)
    markup.add(btn2)
    return markup
