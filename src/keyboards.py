from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from src.core.buttons import Buttons


async def main_kb(is_admin: bool):
    kb_list = [
        [KeyboardButton(text=Buttons.tariff), KeyboardButton(text=Buttons.tariff)],
        [KeyboardButton(text=Buttons.subscription), KeyboardButton(text=Buttons.support)]
    ]
    if is_admin:
        kb_list.append([KeyboardButton(text=Buttons.admin)])
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
