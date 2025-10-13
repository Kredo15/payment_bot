from aiogram_i18n import LazyProxy
from aiogram_i18n.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from src.core.settings import settings


def kb_chanel():
    buttons = [
        [
            InlineKeyboardButton(text=LazyProxy("to_payment"), url=settings.URL_CHANEL),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def back_to_profile():
    buttons = [
        [
            InlineKeyboardButton(text=LazyProxy("back"), callback_data="profile_button"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
