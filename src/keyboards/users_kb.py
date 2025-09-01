from aiogram_i18n import LazyProxy
from aiogram_i18n.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import get_subscriptions


async def main_kb():
    kb_list = [
        [
            KeyboardButton(text=LazyProxy("tariff_button")),
            KeyboardButton(text=LazyProxy("profile_button"))
        ],
        [
            KeyboardButton(text=LazyProxy("subscription_button")),
            KeyboardButton(text=LazyProxy("support_button"))
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return keyboard


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


async def kb_tariff(session: AsyncSession) -> InlineKeyboardMarkup:
    subscriptions = await get_subscriptions(session)
    buttons = [
        [
            InlineKeyboardButton(
                text=LazyProxy(
                    'subscription',
                    duration_days=subscription.duration_days,
                    price=subscription.price,
                    currency=subscription.currency
                ),
                callback_data=f"subscription_{subscription.price}")
        ]
        for subscription in subscriptions
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
