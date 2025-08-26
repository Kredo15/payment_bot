from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from src.utils import get_admins


async def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="💳 Тарифные планы"), KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="🔑 Моя подписка"), KeyboardButton(text="🤝 Поддержка")]
    ]
    admins = await get_admins()
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return keyboard


def get_kb_buy() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text='Подписка | 30 дней | 100 RUB', callback_data="buy_one")],
        [InlineKeyboardButton(text='Подписка | 90 дней | 250 RUB', callback_data="buy_three")],
        [InlineKeyboardButton(text='Подписка | 180 дней | 450 RUB', callback_data="buy_six")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
