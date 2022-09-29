from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from databases.models.user import User


class AuthorizedFilter(BoundFilter):
    key='authorized'

    def __init__(self, authorized=True):
        self.authorized = authorized

    async def check(self, message: types.Message) -> bool:
        user = ctx_data.get()['user']
        return user.is_authorized() == self.authorized