from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.answers import *
from bot.filters.has_name import HasNameFilter
from bot.handlers.profile import send_menu
from bot.keyboards.reply.is_name_right_markup import get_name_right_markup
from bot.models.states.sign_in_states import SignInStates
from databases.models.user import User


async def default_name_reply(message: types.Message, user: User):
    print('Got message: ' + message.text)
    if message.text == is_name_right_markup_answers['right']:
        user.name = message.from_user.first_name
        await SignInStates.waiting_group.set()
        await message.answer(enter_group_message, reply_markup=None)
    elif message.text == is_name_right_markup_answers['wrong']:
        await SignInStates.waiting_name.set()
        await message.answer(wrong_name_reply_message, reply_markup=None)
    else:
        await message.answer(check_name_message(message.from_user.first_name), reply_markup=get_name_right_markup())


async def name_entered(message: types.Message, user: User):
    user.name = message.text
    await message.answer(name_entered_message(message.text))
    if not user.has_group():
        await SignInStates.waiting_group.set()
        await message.answer(enter_group_message)


async def group_entered(message: types.Message, user: User, state: FSMContext):
    user.group = message.text
    await message.answer(group_entered_message)
    await state.finish()
    await send_menu(message.bot, user)


def register_sign_in(dp: Dispatcher):
    dp.register_message_handler(default_name_reply, state=SignInStates.waiting_name_reply)
    dp.register_message_handler(name_entered, state=SignInStates.waiting_name)
    dp.register_message_handler(group_entered, state=SignInStates.waiting_group)