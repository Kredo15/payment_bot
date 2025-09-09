import pytest
from typing import Any

from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType, TelegramMethod
from aiogram_i18n.cores import BaseCore
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.mocked_bot import MockedBot
from tests.utils.updates import get_message, get_update, get_user
from tests.utils.for_test import create_test_subscriptions


@pytest.mark.parametrize(
    "language_code",
    [
        "ru",
        "en"
    ],
)
@pytest.mark.asyncio
async def test_tariff_command(
        bot: MockedBot,
        dispatcher: Dispatcher,
        core: BaseCore[Any],
        async_test_session: AsyncSession,
        language_code: str
):
    await create_test_subscriptions(async_test_session)
    bot.add_result_for(
        method=SendMessage,
        ok=True
    )
    await core.startup()
    button = core.get("profile_button", language_code)
    user = get_user(language_code)
    message = get_message(button, from_user=user)
    update = get_update(message)
    result = await dispatcher.feed_update(
        bot=bot,
        update=update
    )
    assert result is not UNHANDLED
    outgoing_message: TelegramMethod[TelegramType] = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    correct_message = core.get(
        "profile_message",
        language_code,
        telegram_id=message.from_user.id,
        time_zone='UTC',
        email='Empty'
    )
    assert outgoing_message.text == correct_message
    assert outgoing_message.reply_markup is not None
