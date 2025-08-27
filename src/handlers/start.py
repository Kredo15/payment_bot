from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import dp
from src.core.message import AnswerMessage
from src.keyboards import main_kb, get_kb_buy
from src.utils import check_admin


@dp.message(CommandStart())
async def start_command(message: Message, session: AsyncSession):
    is_admin = await check_admin(message.from_user.id, session)
    await message.answer(
        text='Выбери действие',
        reply_markup=await main_kb(is_admin)
    )


@dp.callback_query(F.data == "info")
async def choose_category(callback: CallbackQuery):
    await callback.message.answer(
        text=AnswerMessage.info
    )


@dp.callback_query(F.data == "tariff")
async def choose_category(callback: CallbackQuery):
    await callback.message.answer(
        text=AnswerMessage.tariff,
        reply_markup=get_kb_buy()
    )


@dp.callback_query(F.data == "transactions")
async def choose_category(callback: CallbackQuery):
    await callback.message.answer(
        text='История транзаций'
    )


@dp.callback_query(F.data == "contact")
async def choose_category(callback: CallbackQuery):
    await callback.message.answer(
        text='В случае каких-либо вопросов пишите:\n@ivankredo'
    )
