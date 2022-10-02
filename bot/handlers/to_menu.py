from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from bot.filters.authorized import AuthorizedFilter
from bot.handlers.profile import send_menu
from databases.models.user import User


async def to_menu(query: CallbackQuery, user: User):
    await send_menu(query.bot, user)

def register_to_menu(dp: Dispatcher):
    dp.register_callback_query_handler(to_menu, AuthorizedFilter(), text=['to_menu'])