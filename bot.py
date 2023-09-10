import asyncio
import json
import logging
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.config import load_config
from bot.filters.authorized import AuthorizedFilter
from bot.filters.has_group import HasGroupFilter
from bot.filters.has_name import HasNameFilter
from bot.filters.is_admin import IsAdmin
from bot.handlers.admin import register_admin
from bot.handlers.hello import register_hello
from bot.handlers.profile import register_profile
from bot.handlers.settings import register_settings
from bot.handlers.sign_in import register_sign_in
from bot.handlers.to_menu import register_to_menu
from bot.middlewares.texts import TextsMiddleware
from bot.middlewares.users_database import UsersDatabaseMiddleware
from bot.misc.users_dbm import UsersDBM
from lexicon import lexicon

logger = logging.getLogger(__name__)

DEBUG_MODE = True

def register_all_middlewares(dp: Dispatcher):
    dp.setup_middleware(UsersDatabaseMiddleware(UsersDBM('users')))
    dp.setup_middleware(TextsMiddleware())


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AuthorizedFilter)
    dp.filters_factory.bind(HasNameFilter)
    dp.filters_factory.bind(HasGroupFilter)
    dp.filters_factory.bind(IsAdmin)


def register_all_handlers(dp: Dispatcher):
    register_hello(dp)
    register_sign_in(dp)
    register_profile(dp)
    register_settings(dp)
    register_to_menu(dp)
    register_admin(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )
    config = load_config('.env')

    loop = asyncio.get_event_loop()
    if DEBUG_MODE:
        bot = Bot(token=config.tg_bot.debug_token, parse_mode='HTML')
    else:
        bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage, loop=loop)
    dp.bot['config'] = config

    users_dbm = UsersDBM('users')

    dp.bot['users_dbm'] = users_dbm
    dp.bot['lexicon'] = lexicon

    with open('ru_RU.json', 'r') as f:
        json_texts = json.load(f)
        dp.bot['texts'] = json_texts

    print('BOT IS READY TO START')

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
