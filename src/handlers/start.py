from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.app import dp
from src.core.message import AnswerMessage
from src.keyboards import main_kb, get_kb_buy


@dp.message(Command(commands=["start", "menu"]))
async def start_command(message: Message):
    await message.answer(
        text='Выбери действие',
        reply_markup=await main_kb(message.from_user.id)
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
