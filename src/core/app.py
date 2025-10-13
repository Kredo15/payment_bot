import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from src.core.settings import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(
    token=settings.API_KEY_BOT,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)
storage = RedisStorage.from_url(settings.redis_settings.redis_url)
dp = Dispatcher(storage=storage)


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    logging.info("Бот запущен!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.session.close()
    logging.info("Соединения закрыты.")


async def run_bot():
    from src.middleware import setup_middleware
    from src.handlers import setup_routers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    setup_middleware(dp)
    setup_routers(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:  # нормальное завершение
        logger.info("Polling cancelled.")
        raise
    finally:
        await dp.storage.close()
        await bot.session.close()
        logger.info("Bot session closed.")
