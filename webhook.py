from aiohttp import web

from src.service.cryptopay import crypto, close_session
from src.service.yoomoney_api import yookassa_webhook_handler


def setup():
    web_app = web.Application()
    web_app.router.add_post("/crypto-secret-path", crypto.get_updates)
    web_app.router.add_post("/yookassa", yookassa_webhook_handler)
    web_app.on_shutdown.append(close_session)
    web.run_app(app=web_app, host="localhost", port=3001)


if __name__ == "__main__":
    setup()
