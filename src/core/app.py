import logging
import asyncio
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

    logging.info("Бот запущен!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    from src.webhook.cryptopay import close_session

    await dp.storage.close()
    await redis_client.close()
    await close_session(app)
    await bot.delete_webhook()
    await bot.session.close()

    logging.info("Соединения закрыты.")


async def setup_webhook() -> None:
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
    from aiohttp.web import AppRunner, TCPSite

    await bot.set_webhook(
        settings.webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        secret_token=settings.WEBHOOK_SECRET,
        drop_pending_updates=True
    )

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, host=settings.WEBHOOK_HOST, port=settings.WEBHOOK_PORT)
    await site.start()

    await asyncio.Event().wait()


async def run_bot():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await redis_client.init_redis()
    await setup_webhook()
