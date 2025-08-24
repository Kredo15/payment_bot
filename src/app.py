import logging

from aiogram import Bot, Dispatcher

from src.core.settings import settings

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.API_KEY_BOT)
dp = Dispatcher()


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    logging.info("Бот запущен!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.session.close()
    logging.info("Соединения закрыты.")


def run_bot():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.run_polling(bot)
