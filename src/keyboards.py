from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


def get_main_bk():
    buttons = [
        [InlineKeyboardButton(text='Информация', callback_data="info")],
        [InlineKeyboardButton(text='Тарифы', callback_data="tariff")],
        [InlineKeyboardButton(text='История', callback_data="transactions")],
        [InlineKeyboardButton(text='Контакты', callback_data="contact")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
