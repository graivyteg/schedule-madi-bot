from aiogram import Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.answers import is_name_right_markup_answers


def get_text_correct_markup(bot: Bot) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    answers = bot['texts']['text_correct_markup']
    btn1 = KeyboardButton(answers['right'])
    btn2 = KeyboardButton(answers['wrong'])
    markup.add(btn1)
    markup.add(btn2)
    return markup
