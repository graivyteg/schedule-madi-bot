from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.answers import *
from bot.filters.has_name import HasNameFilter
from bot.handlers.profile import send_menu
from bot.keyboards.reply.text_correct_markup import get_text_correct_markup
from bot.models.states.sign_in_states import SignInStates
from databases.models.user import User


async def default_name_reply(message: types.Message, user: User):
    answers = message.bot['texts']
    if message.text == answers['text_correct_markup']['right']:
        user.name = message.from_user.first_name
        await SignInStates.waiting_group.set()
        await message.answer(answers['enter_group'])
    elif message.text == answers['text_correct_markup']['wrong']:
        await SignInStates.waiting_name.set()
        await message.answer(answers['enter_name'])
    else:
        await message.answer(answers['confirm_name'],
                             reply_markup=get_text_correct_markup(message.bot))


async def name_entered(message: types.Message, user: User):
    user.name = message.text
    answers = message.bot['texts']
    await message.answer(answers['name_confirmed'].format(message.text))
    if not user.has_group():
        await SignInStates.waiting_group.set()
        await message.answer(enter_group_message)


async def group_entered(message: types.Message, user: User, state: FSMContext):
    user.group = message.text
    await message.answer(message.bot['texts']['group_entered'])
    await state.finish()
    await send_menu(message.bot, user)


def register_sign_in(dp: Dispatcher):
    dp.register_message_handler(default_name_reply, state=SignInStates.waiting_name_reply)
    dp.register_message_handler(name_entered, state=SignInStates.waiting_name)
    dp.register_message_handler(group_entered, state=SignInStates.waiting_group)