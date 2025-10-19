from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton


def referral() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=LazyProxy("invite_friend"), callback_data="invite_friend"
            ),
            InlineKeyboardButton(
                text=LazyProxy("my_referral_button"), callback_data="my_referrals"
            ),
        ],
        [InlineKeyboardButton(text=LazyProxy("back"), callback_data="profile_button")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def back_to_referral_info() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=LazyProxy("back"), callback_data="referral_info")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
