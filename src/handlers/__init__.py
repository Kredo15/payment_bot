from __future__ import annotations
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Dispatcher, Router

from . import admins, users, payments, subscription, profile

logger = logging.getLogger("handlers")

all_routers: list[Router] = [
    users.router,
    payments.router,
    subscription.router,
    profile.router
]


def setup_routers(dp: Dispatcher) -> None:
    dp.include_routers(*all_routers)

    logger.debug("%s routers has been load", len(all_routers))


__all__ = ["setup_routers"]
