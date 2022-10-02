from aiogram.dispatcher.filters.state import StatesGroup, State


class SettingsStates(StatesGroup):
    changing_name = State()
    changing_group = State()