from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.filters.authorized import AuthorizedFilter
from bot.handlers.profile import send_menu
from bot.keyboards.inline.settings import get_settings_markup
from bot.models.states.settings_states import SettingsStates
from databases.models.user import User


async def open_settings(message: Message, user: User, texts):
    await message.answer(texts['settings_menu'], reply_markup=get_settings_markup(texts))


async def open_settings_query(query: CallbackQuery, user: User, texts):
    await open_settings(query.message, user, texts)


async def change_name(query: CallbackQuery, user: User, texts):
    await SettingsStates.changing_name.set()
    await query.message.answer(texts['enter_name'])


async def change_group(query: CallbackQuery, user: User, texts):
    await SettingsStates.changing_group.set()
    await query.message.answer(texts['enter_group'])


async def name_changed(message: Message, user: User, texts, state: FSMContext):
    user.name = message.text
    await state.finish()
    await message.answer(texts['name_changed'].format(user.name))
    await open_settings(message, user, texts)

async def group_changed(message: Message, user: User, texts, state: FSMContext):
    user.group = message.text
    await state.finish()
    await message.answer(texts['group_changed'].format(user.group))
    await open_settings(message, user, texts)


async def to_menu(query: CallbackQuery, user: User):
    await send_menu(query.bot, user)


def register_settings(dp: Dispatcher):
    dp.register_callback_query_handler(open_settings_query, AuthorizedFilter(), text=['open_settings'])
    dp.register_callback_query_handler(change_name, AuthorizedFilter(), text=['change_name'])
    dp.register_callback_query_handler(change_group, AuthorizedFilter(), text=['change_group'])
    dp.register_callback_query_handler(to_menu, text=['to_menu'])
    dp.register_message_handler(name_changed, AuthorizedFilter(), state=SettingsStates.changing_name)
    dp.register_message_handler(group_changed, AuthorizedFilter(), state=SettingsStates.changing_group)