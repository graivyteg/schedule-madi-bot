from datetime import datetime

from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.answers import get_menu
from bot.filters.authorized import AuthorizedFilter
from bot.keyboards.inline.even_odd_week import get_even_odd_markup
from bot.keyboards.inline.profile import get_profile_keyboard
from bot.keyboards.inline.settings import get_settings_markup
from bot.keyboards.inline.to_menu import get_to_menu_markup
from bot.keyboards.inline.weekday import get_weekday_markup
from bot.models.states.week_states import WeekStates
from databases.models.user import User
from madi_api.even_odd_loader import EvenOddLoader
from madi_api.network_loader import NetworkScheduleLoader


async def send_menu(bot: Bot, user: User):
    await bot.send_message(user.id,
                           bot['texts']['profile_menu'].format(user.name, user.group),
                           reply_markup=get_profile_keyboard(bot['texts']))

async def send_menu_message(message: Message, user: User):
    await message.edit_text(message.bot['texts']['profile_menu'].format(user.name, user.group),
                           reply_markup=get_profile_keyboard(message.bot['texts']))


async def send_schedule(query: CallbackQuery, user: User, texts):
    schedule = await NetworkScheduleLoader(user.group).load_schedule()
    for i in range(0, 6):
        await query.message.edit_text(str(schedule.get_schedule_at_day(i)),
                                   reply_markup=get_to_menu_markup(texts))


async def get_schedule(user: User):
    schedule = await NetworkScheduleLoader(user.group).load_schedule()
    weekday = datetime.today().weekday()
    workday = schedule.get_schedule_at_day(weekday)
    is_odd = await EvenOddLoader().is_today_odd()
    return weekday, workday, is_odd

async def send_schedule_today(query: CallbackQuery, user: User, texts):
    weekday, workday, is_odd = await get_schedule(user)
    await query.message.edit_text(workday.str_even_odd(is_odd),
                               reply_markup=get_to_menu_markup(texts))


async def send_schedule_today_command(message: Message, user: User, texts):
    weekday, workday, is_odd = await get_schedule(user)
    await message.answer(workday.str_even_odd(is_odd),
                               reply_markup=get_to_menu_markup(texts))


async def get_schedule_tomorrow(user: User):
    schedule = await NetworkScheduleLoader(user.group).load_schedule()
    weekday = (datetime.today().weekday() + 1) % 7
    today = datetime.today()
    tomorrow = datetime(today.year, today.month, today.day + 1)
    is_odd = await EvenOddLoader().is_date_odd(tomorrow)
    return schedule, weekday, is_odd

async def send_schedule_tomorrow(query: CallbackQuery, user: User, texts):
    schedule, weekday, is_odd = await get_schedule_tomorrow(user)
    await query.message.edit_text(schedule.get_schedule_at_day(weekday).str_even_odd(is_odd),
                               reply_markup=get_to_menu_markup(texts))

async def send_schedule_tomorrow_command(message: Message, user: User, texts):
    schedule, weekday, is_odd = await get_schedule_tomorrow(user)
    await message.answer(schedule.get_schedule_at_day(weekday).str_even_odd(is_odd),
                               reply_markup=get_to_menu_markup(texts))

async def send_schedule_week(query: CallbackQuery, user: User, texts):
    await WeekStates.waiting_weekday.set()
    await query.message.edit_text(texts['choose_weekday'], reply_markup=get_weekday_markup(texts))

async def open_weekday_menu(query: CallbackQuery, user: User, texts, state: FSMContext):
    wd = -1
    if query.data == 'to_menu':
        await send_menu_message(query.message, user)
        await state.finish()
        return
    if query.data == 'monday':
        wd = 0
    elif query.data == 'tuesday':
        wd = 1
    elif query.data == 'wednesday':
        wd = 2
    elif query.data == 'thursday':
        wd = 3
    elif query.data == 'friday':
        wd = 4
    elif query.data == 'saturday':
        wd = 5
    schedule = await NetworkScheduleLoader(user.group).load_schedule_by_group(user.group)
    workday = schedule.get_schedule_at_day(wd)
    await query.message.edit_text(str(workday), reply_markup=get_to_menu_markup(texts))
    await state.finish()

async def help(message: Message, texts):
    await message.answer(texts['help'])

def register_profile(dp: Dispatcher):
    dp.register_callback_query_handler(send_schedule, AuthorizedFilter(), text=['get_schedule'])
    dp.register_callback_query_handler(send_schedule_today, AuthorizedFilter(), text=['get_schedule_today'])
    dp.register_callback_query_handler(send_schedule_tomorrow, AuthorizedFilter(), text=['get_schedule_tomorrow'])
    dp.register_callback_query_handler(send_schedule_week, AuthorizedFilter(), text=['get_schedule_week'])
    dp.register_callback_query_handler(open_weekday_menu, AuthorizedFilter(), state=WeekStates.waiting_weekday)

    dp.register_message_handler(send_schedule_today_command,  AuthorizedFilter(), commands=['today'])
    dp.register_message_handler(send_schedule_tomorrow_command, AuthorizedFilter(), commands=['tomorrow'])
    dp.register_message_handler(help, commands=['help'])

