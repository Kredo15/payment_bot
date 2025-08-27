from aiogram import F
from aiogram.types import Message

from src.app import dp
from src.core.buttons import Buttons
from src.core.message import AnswerMessage
from src.keyboards import get_kb_buy


@dp.message(F.text == Buttons.tariff)
async def tariff(message: Message):
    await message.answer(
        text=AnswerMessage.tariff,
        reply_markup=get_kb_buy()
    )
