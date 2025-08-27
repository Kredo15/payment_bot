from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import dp
from src.keyboards import main_kb
from src.utils import check_admin


@dp.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext, session: AsyncSession):
    is_admin = await check_admin(message.from_user.id, session)
    name = message.from_user.full_name
    await message.answer(
        text=i18n.hello(user=name, language=i18n.locale),
        reply_markup=await main_kb(is_admin)
    )
