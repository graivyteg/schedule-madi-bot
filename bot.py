import asyncio
import logging
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.config import load_config
from bot.handlers.hello import register_hello
from bot.handlers.profile import register_profile
from bot.handlers.sign_in import register_sign_in
from bot.middlewares.users_database import UsersDatabaseMiddleware
from databases.users_dbm import UsersDBM

logger = logging.getLogger(__name__)


def register_all_middlewares(dp: Dispatcher):
    dp.setup_middleware(UsersDatabaseMiddleware(UsersDBM('users')))


def register_all_filters(dp: Dispatcher):
    pass


def register_all_handlers(dp: Dispatcher):
    register_hello(dp)
    register_sign_in(dp)
    register_profile(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )
    config = load_config('.env')

    loop = asyncio.get_event_loop()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage, loop=loop)
    dp.bot['config'] = config

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
