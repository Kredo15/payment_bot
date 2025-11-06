import logging
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from src.core.settings import settings
from src.cache.redis_client import RedisCache

logger = logging.getLogger(__name__)

bot = Bot(
    token=settings.API_KEY_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
storage = RedisStorage.from_url(settings.redis_url)
redis_client = RedisCache()
dp = Dispatcher(storage=storage)
app = web.Application()


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    from src.middleware import setup_middleware
    from src.handlers import setup_routers
    from src.middleware.prometheus import prometheus_middleware_factory
    from src.webhook.metrics import MetricsView
    from src.webhook.cryptopay import crypto
    from src.webhook.yookassa_api import yookassa_webhook_handler

    setup_middleware(dp)
    setup_routers(dp)

    app.middlewares.append(prometheus_middleware_factory())
    app.router.add_route("GET", "/metrics", MetricsView)
    app.router.add_route("POST", "/crypto-secret-path", crypto.get_updates)
    app.router.add_route("POST", "/yookassa", yookassa_webhook_handler)

    await bot.set_webhook(
        settings.webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        secret_token=settings.WEBHOOK_SECRET
    )
    await redis_client.init_redis()
    await bot.send_message(chat_id=settings.ADMIN, text='Бот запущен!')

    logging.info("Старт!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    from src.webhook.cryptopay import close_session

    await dp.storage.close()
    await redis_client.close()
    await close_session(app)
    await bot.delete_webhook()
    await bot.session.close()

    logging.info("Соединения закрыты.")


def setup_webhook() -> None:
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)


def run_bot():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    setup_webhook()
    web.run_app(app, host=settings.WEBHOOK_HOST, port=settings.WEBHOOK_PORT)
