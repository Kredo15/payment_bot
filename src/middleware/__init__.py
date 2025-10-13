from __future__ import annotations
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Dispatcher

from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from . import db_session, i18n_middleware
from src.core.db_dependency import async_session_maker

logger = logging.getLogger("middleware")


def setup_middleware(dp: Dispatcher) -> None:
    i18n = I18nMiddleware(
        core=FluentRuntimeCore(
            path="locales/{locale}/LC_MESSAGES",
            raise_key_error=False
        ),
        manager=i18n_middleware.UserManager(),
        default_locale="ru"
    )
    dp.message.middleware(db_session.DBSessionMiddleware(async_session_maker))
    dp.callback_query.middleware(db_session.DBSessionMiddleware(async_session_maker))
    i18n.setup(dispatcher=dp)
