from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_settings_markup():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Изменить имя', callback_data='change_name')
    btn2 = InlineKeyboardButton('Изменить группу', callback_data='change_group')
    btn3 = InlineKeyboardButton('Вернуться в меню', callback_data='to_menu')
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    return markup
