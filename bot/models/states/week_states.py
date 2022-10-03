from aiogram.dispatcher.filters.state import StatesGroup, State


class WeekStates(StatesGroup):
    waiting_even_odd = State()
    waiting_weekday = State()