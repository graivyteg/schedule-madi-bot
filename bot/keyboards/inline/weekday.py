from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_weekday_markup(texts):
    t = texts['weekday_markup']
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(t['monday'], callback_data='monday')
    btn2 = InlineKeyboardButton(t['tuesday'], callback_data='tuesday')
    btn3 = InlineKeyboardButton(t['wednesday'], callback_data='wednesday')
    btn4 = InlineKeyboardButton(t['thursday'], callback_data='thursday')
    btn5 = InlineKeyboardButton(t['friday'], callback_data='friday')
    btn6 = InlineKeyboardButton(t['saturday'], callback_data='saturday')
    btn7 = InlineKeyboardButton(texts['to_menu'], callback_data='to_menu')
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    markup.add(btn5)
    markup.add(btn6)
    markup.add(btn7)
    return markup