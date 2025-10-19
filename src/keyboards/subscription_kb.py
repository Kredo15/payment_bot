from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from src.cruds.subscription_crud import get_subscriptions


async def kb_tariff(session: AsyncSession) -> InlineKeyboardMarkup:
    subscriptions = await get_subscriptions(session)
    buttons = [
        [
            InlineKeyboardButton(
                text=LazyProxy(
                    "subscription",
                    duration_days=subscription.duration_days,
                    price=subscription.price,
                    currency=subscription.currency,
                ),
                callback_data=f"subscription_{subscription.name}",
            )
        ]
        for subscription in subscriptions
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def kb_payment():
    buttons = [
        [
            InlineKeyboardButton(text=LazyProxy("pay"), callback_data="pay"),
        ],
        [InlineKeyboardButton(text=LazyProxy("back"), callback_data="tariff_button")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
