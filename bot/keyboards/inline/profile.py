from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_profile_keyboard(texts) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    t = texts['profile_markup']
    #btn1 = InlineKeyboardButton('Посмотреть расписание', callback_data='get_schedule')
    btn1 = InlineKeyboardButton(t['today_schedule'], callback_data='get_schedule_today')
    btn2 = InlineKeyboardButton(t['tomorrow_schedule'], callback_data='get_schedule_tomorrow')
    btn3 = InlineKeyboardButton(t['week_schedule'], callback_data='get_schedule_week')
    btn4 = InlineKeyboardButton(t['settings'], callback_data='open_settings')
    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    keyboard.add(btn4)
    return keyboard

