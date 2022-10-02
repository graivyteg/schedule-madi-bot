from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.answers import *
from bot.filters.authorized import AuthorizedFilter
from bot.filters.has_name import HasNameFilter
from bot.handlers.profile import send_menu
from bot.keyboards.reply.text_correct_markup import get_text_correct_markup
from bot.models.states.sign_in_states import SignInStates
from databases.models.user import User


async def start_non_authorized(message: types.Message, user: User):
    await message.answer(message.bot['texts']['start_non_authorized'])
    if not user.has_name():
        await SignInStates.waiting_name_reply.set()
        await message.answer(message.bot['texts']['confirm_name'].format(message.from_user.first_name),
                             reply_markup=get_text_correct_markup(message.bot))
    elif not user.has_group():
        await SignInStates.waiting_group.set()


async def start_authorized(message: types.Message, user: User):
    await message.answer(message.bot['texts']['start_authorized'].format(user.name))
    await send_menu(message.bot, user)


def register_hello(dp: Dispatcher):
    dp.register_message_handler(start_non_authorized, AuthorizedFilter(False), commands=['start'])
    dp.register_message_handler(start_authorized, AuthorizedFilter(), commands=['start'])
