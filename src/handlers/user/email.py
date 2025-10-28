from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram_i18n import I18nContext
from aiogram.fsm.context import FSMContext

from src.cruds.user_crud import update_email
from src.keyboards.common_kb import back_to_profile
from src.state.email import EmailState
from src.service.utils import valid_email
from src.handlers.user.profile import profile_message

router = Router()


@router.callback_query(F.data == "email")
async def email(callback: CallbackQuery, i18n: I18nContext, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text=i18n.change_email(), reply_markup=back_to_profile()
    )
    await state.set_state(EmailState.change_email)
    data = await state.get_data()
    data['user_id'] = callback.from_user.id
    await state.update_data(data)


@router.message(EmailState.change_email)
async def change_email(
    message: Message, i18n: I18nContext, state: FSMContext, session: AsyncSession
):
    if valid_email(message.text):
        await update_email(message.from_user.id, message.text, session)
        data = await state.get_data()
        await profile_message(message, data['user_id'], i18n, state, session)
    else:
        await message.answer(text=i18n.not_valid_email())
