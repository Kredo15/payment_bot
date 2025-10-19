from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_choose_method():
    buttons = [
        [
            InlineKeyboardButton(text=LazyProxy("crypt"), callback_data="crypt"),
            InlineKeyboardButton(text=LazyProxy("yookassa"), callback_data="yookassa"),
            InlineKeyboardButton(text=LazyProxy("back"), callback_data="tariff_button"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def kb_payment(url: str):
    buttons = [
        [
            InlineKeyboardButton(text=LazyProxy("to_payment"), url=url),
            InlineKeyboardButton(text=LazyProxy("back"), callback_data="pay"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
