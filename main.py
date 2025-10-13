import asyncio
import logging

from core.app import run_bot

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен пользователем.")
    except Exception:
        logger.exception("Критическая ошибка при запуске")
