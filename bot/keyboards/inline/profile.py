from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_profile_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    #btn1 = InlineKeyboardButton('Посмотреть расписание', callback_data='get_schedule')
    btn1 = InlineKeyboardButton('Расписание на сегодня', callback_data='get_schedule_today')
    btn2 = InlineKeyboardButton('Расписание на завтра', callback_data='get_schedule_tomorrow')
    btn3 = InlineKeyboardButton('Настройки', callback_data='open_settings')
    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    return keyboard
