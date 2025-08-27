import logging

from aiogram import Bot, Dispatcher
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from src.core.settings import settings
from src.core.db_dependency import async_session_maker
from src.middleware import DBSessionMiddleware, i18n_middleware

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
    i18n = I18nMiddleware(
        core=FluentRuntimeCore(
            path="locales/{locale}/LC_MESSAGES",
            # path="locales/{locale}"
        ),
        # передаем наш кастомный менеджер языка из middlewares/i18n_middleware.py
        manager=i18n_middleware.UserManager(),
        default_locale="ru"
    )
    dp.message.middleware(DBSessionMiddleware(async_session_maker))
    i18n.setup(dispatcher=dp)
    dp.run_polling(bot)
