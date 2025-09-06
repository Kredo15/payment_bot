from datetime import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Chat, Message, Update, User

TEST_USER = User(
    id=123,
    is_bot=False,
    first_name="Test",
    last_name="Bot",
    username="testbot",
    language_code="ru",
    is_premium=True
)

TEST_CHAT = Chat(
    id=123,
    type="private",
    username=TEST_USER.username,
    first_name=TEST_USER.first_name,
    last_name=TEST_USER.last_name,
)

TEST_MESSAGE = Message(message_id=123, date=datetime.now(), chat=TEST_CHAT)


def get_user(language_code: str):
    return User(
        id=123,
        is_bot=False,
        first_name="Test",
        last_name="Bot",
        username="testbot",
        language_code=language_code,
        is_premium=True
    )


def get_message(text: str, chat=TEST_CHAT, from_user=TEST_USER):
    return Message(
        message_id=123,
        date=datetime.now(),
        chat=chat,
        from_user=from_user,
        sender_chat=TEST_CHAT,
        text=text
    )


def get_chat(
        id: int = None,
        type: str = "private",
        title: str = "TEST_TITLE",
        username: str = TEST_CHAT.username,
        *args,
        **kwargs
) -> Chat:
    return Chat(
        id=id,
        type=type,
        title=title,
        username=username,
        first_name=TEST_USER.first_name,
        last_name=TEST_USER.last_name,
        *args,
        **kwargs
    )


def get_callback_query(data: str | CallbackData, from_user=TEST_USER, message=None):
    return CallbackQuery(
        id="test",
        from_user=from_user,
        chat_instance="test",
        message=message or TEST_MESSAGE,
        data=data,
    )


def get_update(message: Message = None, callback_query: CallbackQuery = None):
    return Update(
        update_id=123,
        message=message,
        callback_query=callback_query
    )
