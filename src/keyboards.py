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


def get_kb_buy() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text='Оплатить 1 месяц', callback_data="buy_one")],
        [InlineKeyboardButton(text='Оплатить 3 месяца', callback_data="buy_three")],
        [InlineKeyboardButton(text='Оплатить 6 месяцев', callback_data="buy_six")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
