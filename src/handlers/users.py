from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram_i18n import I18nContext, LazyProxy

from src.cruds.user_crud import check_user
from src.keyboards.users_kb import main_kb

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext, session: AsyncSession):
    await message.answer(
        text=i18n.hello(),
        reply_markup=main_kb()
    )
    await check_user(message.from_user.id, session)


@router.message(F.text == LazyProxy("support_button"))
async def support(message: Message, i18n: I18nContext):
    await message.answer(
        text=i18n.support_message()
    )
