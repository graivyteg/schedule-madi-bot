from databases.models.user import User


def start_non_authorized_message(username: str):
    return f'Привет! Я бот, который поможет тебе быстро получить своё расписание.'


def start_authorized_message(username: str):
    return f'С возвращением, {username}! Продолжим работу?'


def check_name_message(username: str):
    return f'Тебя зовут {username}, всё верно?'


wrong_name_reply_message = 'Хорошо, тогда введи своё имя'
enter_group_message = 'Пожалуйста, введи свою группу:'
is_name_right_markup_answers = {'right': 'Да, всё верно', 'wrong': 'Нет, ввести другое'}


def name_entered_message(username: str):
    return f'Отлично! Буду звать тебя {username}!'


group_entered_message = 'Отлично, теперь я знаю твою группу!'


def get_menu(user: User):
    return '<b>Главное меню</b>\n' + \
           f'Твоё имя: <i>{user.name}</i>\n' + \
           f'Твоя группа: <i>{user.group}</i>\n\n' + \
           'Выбери действие:'
