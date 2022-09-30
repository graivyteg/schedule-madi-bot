from datetime import datetime

from aiogram import types, Bot, Dispatcher
from aiogram.types import CallbackQuery

from bot.answers import get_menu
from bot.filters.authorized import AuthorizedFilter
from bot.keyboards.inline.profile import get_profile_keyboard
from databases.models.user import User
from schedule_loader.loader import ScheduleLoader


async def send_menu(bot: Bot, user: User):
    await bot.send_message(user.id, get_menu(user), reply_markup=get_profile_keyboard())


async def send_schedule(query: CallbackQuery, user: User):
    loader = ScheduleLoader(user.group)
    schedule = await loader.load_schedule()
    for i in range(0, 6):
        await query.message.answer(str(schedule.get_schedule(i)))

async def send_schedule_today(query: CallbackQuery, user: User):
    loader = ScheduleLoader(user.group)
    schedule = await loader.load_schedule()
    weekday = datetime.today().weekday()
    await query.message.answer(str(schedule.get_schedule(weekday)))

async def send_schedule_tomorrow(query: CallbackQuery, user: User):
    loader = ScheduleLoader(user.group)
    schedule = await loader.load_schedule()
    weekday = datetime.today().weekday() + 1 % 7
    await query.message.answer(str(schedule.get_schedule(weekday)))

def register_profile(dp: Dispatcher):
    dp.register_callback_query_handler(send_schedule, AuthorizedFilter(), text=['get_schedule'])
    dp.register_callback_query_handler(send_schedule_today, AuthorizedFilter(), text=['get_schedule_today'])
    dp.register_callback_query_handler(send_schedule_tomorrow, AuthorizedFilter(), text=['get_schedule_tomorrow'])
