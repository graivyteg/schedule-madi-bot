from aiogram.dispatcher.filters.state import StatesGroup, State


class SignInStates(StatesGroup):
    waiting_name_reply = State()
    waiting_name = State()
    waiting_group = State()


