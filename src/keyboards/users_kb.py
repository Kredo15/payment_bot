from aiogram_i18n import LazyProxy
from aiogram_i18n.types import ReplyKeyboardMarkup, KeyboardButton


def main_kb():
    kb_list = [
        [
            KeyboardButton(text=LazyProxy("tariff_button")),
            KeyboardButton(text=LazyProxy("profile_button")),
        ],
        [
            KeyboardButton(text=LazyProxy("my_subscription_button")),
            KeyboardButton(text=LazyProxy("support_button")),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return keyboard
