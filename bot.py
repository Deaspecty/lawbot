import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config.config import BOT_TOKEN
from handlers.user import auth, home, consult
from middlewares.db import DbMiddleware

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    scheduler = AsyncIOScheduler(
         timezone='Asia/Aqtobe'
    )
    dp = Dispatcher(storage=storage)
    dp.message.middleware(DbMiddleware())
    dp.callback_query.middleware(DbMiddleware())
    dp.include_routers(auth.router, consult.router, home.router)

    bot_me = await bot.me()
    logging.info(
        f'starting bot: @{bot_me.username}'
    )

    # start
    try:
        scheduler.start()
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")