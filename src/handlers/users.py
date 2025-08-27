from aiogram import F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import dp
from src.core.buttons import Buttons
from src.keyboards import get_kb_buy
from src.utils import get_user_data


@dp.message(F.text == Buttons.tariff)
async def tariff(message: Message):
    await message.answer(
        text='Продукт: Закрытый канал',
        reply_markup=get_kb_buy()
    )


@dp.message(F.text == Buttons.profile)
async def tariff(message: Message, session: AsyncSession):
    user_data = await get_user_data(message.from_user.id, session)
    text = "👤 Профиль\n\n"
    await message.answer(
        text=text,
        reply_markup=get_kb_buy()
    )
