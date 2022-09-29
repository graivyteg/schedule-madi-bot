from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from databases.models.user import User


class HasGroupFilter(BoundFilter):
    key='has_group'

    def __init__(self, has_group=True):
        self.has_group = has_group

    async def check(self, message: types.Message) -> bool:
        user = ctx_data.get()['user']
        return user.has_group() == self.has_group