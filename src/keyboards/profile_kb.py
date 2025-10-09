from aiogram_i18n import LazyProxy
from aiogram_i18n.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def kb_profile() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text=LazyProxy("language_button"), callback_data="language"),
            InlineKeyboardButton(text=LazyProxy("email_button"), callback_data="email")
        ],
        [InlineKeyboardButton(text=LazyProxy("time_zone_button"), callback_data="time_zone")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def kb_language():
    buttons = [
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="language_ru"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="language_en")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
