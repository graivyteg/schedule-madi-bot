from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin=True):
        self.is_admin = is_admin

    async def check(self, message: types.Message) -> bool:
        id = message.from_user.id
        print(id, message.bot['config'].tg_bot.admins)
        return str(id) in message.bot['config'].tg_bot.admins
