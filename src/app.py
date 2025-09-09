import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.core.settings import settings


logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=settings.API_KEY_BOT,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)
dp = Dispatcher()


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    logging.info("Бот запущен!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.session.close()
    logging.info("Соединения закрыты.")


def run_bot():
    from src.middleware import setup_middleware
    from src.handlers import setup_routers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    setup_middleware(dp)
    setup_routers(dp)
    dp.run_polling(bot)
