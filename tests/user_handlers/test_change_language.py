import pytest
from typing import Any

from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.methods import DeleteMessage, SendMessage
from aiogram.methods.base import TelegramType, TelegramMethod
from aiogram_i18n.cores import BaseCore
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.mocked_bot import MockedBot
from tests.utils.updates import get_callback_query, get_update, get_user
from tests.utils.for_test import create_test_subscriptions
from src.keyboards.users_kb import main_kb


@pytest.mark.parametrize(
    "language_code, choose_language",
    [
        ("ru", "language_ru"),
        ("en", "language_en")
    ],
)
@pytest.mark.asyncio
async def test_language_command(
        bot: MockedBot,
        dispatcher: Dispatcher,
        core: BaseCore[Any],
        async_test_session: AsyncSession,
        language_code: str,
        choose_language: str
):
    await create_test_subscriptions(async_test_session)
    bot.add_result_for(
        method=SendMessage,
        ok=True
    )
    bot.add_result_for(DeleteMessage, ok=True, result=True)

    await core.startup()
    user = get_user(language_code)
    message = get_callback_query(choose_language, from_user=user)
    update = get_update(callback_query=message)
    result = await dispatcher.feed_update(
        bot=bot,
        update=update
    )
    assert result is not UNHANDLED
    outgoing_message: TelegramMethod[TelegramType] = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == core.get("lang_is_switched", language_code)
    assert outgoing_message.reply_markup == main_kb()
