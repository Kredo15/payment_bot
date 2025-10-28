from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram_i18n import I18nContext, LazyProxy
from aiogram.fsm.context import FSMContext

from src.cruds.user_crud import get_user_data
from src.keyboards.profile_kb import kb_profile

router = Router()


async def profile_message(
    message: Message,
    user_id: int,
    i18n: I18nContext,
    state: FSMContext,
    session: AsyncSession,
):
    data = await state.get_data()
    if data.get('user_id'):
        user_id = data.get('user_id')
    await state.clear()
    user_data = await get_user_data(user_id, session)
    await message.answer(
        text=i18n.profile_message(
            telegram_id=user_id,
            time_zone="UTC",
            email=user_data.get("email") or "Empty",
            language=user_data.get("language") or i18n.locale,
        ),
        reply_markup=kb_profile(),
    )


@router.message(F.text == LazyProxy("profile_button"))
async def profile_button(
    message: Message, i18n: I18nContext, state: FSMContext, session: AsyncSession
):
    await message.delete()
    await profile_message(message, message.from_user.id, i18n, state, session)


@router.callback_query(F.data == "profile_button")
async def profile_callback(
    callback: CallbackQuery, i18n: I18nContext, state: FSMContext, session: AsyncSession
):
    await callback.message.delete()
    await profile_message(
        callback.message, callback.from_user.id, i18n, state, session
    )
