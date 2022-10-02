
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update, CallbackQuery, Message


class TextsMiddleware(BaseMiddleware):
    async def on_pre_process_callback_query(self, query: CallbackQuery, data: dict):
        data['texts'] = query.bot['texts']

    async def on_pre_process_message(self, message: Message, data: dict):
        data['texts'] = message.bot['texts']
