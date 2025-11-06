import logging

from src.core.app import run_bot

# добавляем поток вывода в файл
file_log = logging.FileHandler("app_log.log")
# и вывод в консоль
console_out = logging.StreamHandler()
# указываем эти два потока в настройках логгера
logging.basicConfig(handlers=(file_log, console_out), level=logging.INFO)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        run_bot()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен пользователем.")
    except Exception:
        logger.exception("Критическая ошибка при запуске")
