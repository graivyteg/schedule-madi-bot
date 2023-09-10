from aiogram import Dispatcher
from aiogram.types import Message

from bot.filters.is_admin import IsAdmin
from bot.misc.users_dbm import UsersDBM


async def show_stats(message: Message):
    stats = message.bot['users_dbm'].get_stats()
    await message.answer(message.bot['lexicon'].stats_message(stats))


def register_admin(dp: Dispatcher):
    dp.register_message_handler(show_stats, IsAdmin(), commands=['stats'])