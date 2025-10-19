from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram_i18n import I18nContext, LazyProxy

from service.utils import get_referral
from src.cruds.user_crud import check_user
from src.keyboards.users_kb import main_kb

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext, session: AsyncSession):
    await message.answer(text=i18n.hello(), reply_markup=main_kb())
    referral_id = get_referral(message)
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    await check_user(
        user_id=user_id,
        first_name=first_name,
        username=username,
        referral_id=referral_id,
        session=session,
    )


@router.message(F.text == LazyProxy("support_button"))
async def support(message: Message, i18n: I18nContext):
    await message.answer(text=i18n.support_message())
