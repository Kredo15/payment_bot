import pytest
from typing import Any

from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType, TelegramMethod
from aiogram_i18n.cores import BaseCore

from tests.utils.mocked_bot import MockedBot
from tests.utils.updates import get_message, get_update, get_user
from src.keyboards.users_kb import main_kb


@pytest.mark.parametrize(
    "language_code",
    [
        "ru",
        "en",
    ],
)
@pytest.mark.asyncio
async def test_start_command(
    bot: MockedBot, dispatcher: Dispatcher, core: BaseCore[Any], language_code: str
):
    bot.add_result_for(method=SendMessage, ok=True)
    user = get_user(language_code)
    message = get_message("/start", from_user=user)
    update = get_update(message)
    # Обрабатываем сообщение
    result = await dispatcher.feed_update(bot=bot, update=update)
    assert result is not UNHANDLED
    outgoing_message: TelegramMethod[TelegramType] = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    await core.startup()
    assert outgoing_message.text == core.get(
        "hello", language_code, user=update.message.from_user.full_name
    )
    assert outgoing_message.reply_markup == main_kb()
