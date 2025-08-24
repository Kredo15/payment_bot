from aiogram.filters import Command
from aiogram.types import Message

from src.app import dp
from src.keyboards import get_main_bk


@dp.message(Command(commands=["start", "menu"]))
async def start_command(message: Message):
    await message.answer(
        text='Выбери действие',
        reply_markup=get_main_bk()
    )
