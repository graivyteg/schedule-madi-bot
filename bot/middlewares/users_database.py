from copy import copy

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from databases.models.user import User
from databases.users_dbm import UsersDBM


class UsersDatabaseMiddleware(BaseMiddleware):
    def __init__(self, users_dbm: UsersDBM):
        super().__init__()
        self.dbm = users_dbm

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user = self.dbm.get_or_add_user(message.from_user.id)
        data['user'] = user
        data['old_user'] = copy(user)

    async def on_post_process_message(self, message: types.Message, from_handler, data: dict):
        if not data['old_user'] == data['user']:
            self.dbm.update_user(data['user'])