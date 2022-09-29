from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from databases.models.user import User


class HasNameFilter(BoundFilter):
    key='has_name'

    def __init__(self, has_name=True):
        self.has_name = has_name

    async def check(self, message: types.Message) -> bool:
        user = ctx_data.get()['user']
        return user.has_name() == self.has_name

