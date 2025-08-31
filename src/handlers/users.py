from aiogram import F
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram_i18n import I18nContext, LazyProxy

from src.app import dp
from src.keyboards.users_kb import kb_tariff
from src.utils import get_user_data
from src.keyboards.users_kb import main_kb, kb_profile


@dp.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext):
    name = message.from_user.full_name
    await message.answer(
        text=i18n.hello(user=name, language=i18n.locale),
        reply_markup=await main_kb()
    )


@dp.message(F.text == LazyProxy("tariff-button"))
async def tariff(message: Message, session: AsyncSession):
    await message.answer(
        text='Продукт: Закрытый канал',
        reply_markup=await kb_tariff(session)
    )


@dp.message(F.text == LazyProxy("profile-button"))
async def profile(message: Message, i18n: I18nContext, session: AsyncSession):
    user_data = await get_user_data(message.from_user.id, session)
    await message.answer(
        text=i18n.profile_message(
            telegram_id=message.from_user.id,
            time_zone='UTC',
            email='Empty',
            language=i18n.locale
        ),
        reply_markup=kb_profile()
    )
