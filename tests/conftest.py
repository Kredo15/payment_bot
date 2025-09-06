import pytest
from pathlib import Path
from typing import Any

import pytest_asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import BaseCore
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from src.core.db_dependency import engine
from src.core.settings import settings
from src.database.base_model import Base
from tests.utils.mocked_bot import MockedBot
from src.handlers import setup_routers
from src.middleware import db_session, i18n_middleware
from src.core.db_dependency import async_session_maker


LOCALES = str(
    Path(__file__).parent.parent.joinpath("locales", "{locale}", "LC_MESSAGES").absolute()
)


@pytest_asyncio.fixture(autouse=True)
async def async_db_engine():
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()


@pytest.fixture(scope="session")
def bot():
    return MockedBot()


@pytest.fixture(scope="session")
async def dispatcher():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    core = FluentRuntimeCore(
            path=LOCALES,
            use_isolating=False
        )
    await core.startup()
    i18n_mw = I18nMiddleware(
        core=core,
        manager=i18n_middleware.UserManager(),
        default_locale="ru"
    )
    i18n_mw.setup(dispatcher=dp)
    dp.message.middleware(db_session.DBSessionMiddleware(async_session_maker))
    setup_routers(dp)
    return dp


@pytest.fixture(scope="session")
def core() -> BaseCore[Any]:
    from aiogram_i18n.cores import FluentCompileCore

    return FluentCompileCore(path=LOCALES, use_isolating=False)
