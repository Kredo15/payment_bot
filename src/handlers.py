from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.app import dp
from src.core.message import AnswerMessage
from src.keyboards import get_main_bk


@dp.message(Command(commands=["start", "menu"]))
async def start_command(message: Message):
    await message.answer(
        text='Выбери действие',
        reply_markup=get_main_bk()
    )


@dp.callback_query(F.data == "info")
async def choose_category(callback: CallbackQuery):
    await callback.message.answer(
        text=AnswerMessage.info
    )
