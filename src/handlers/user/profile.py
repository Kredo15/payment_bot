from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram_i18n import I18nContext, LazyProxy
from aiogram.fsm.context import FSMContext

from src.cruds.user_crud import get_user_data, update_email
from src.keyboards.users_kb import main_kb
from src.keyboards.profile_kb import kb_profile, kb_language
from src.keyboards.common_kb import back_to_profile
from src.state.email import EmailState
from src.service.utils import valid_email

router = Router()


async def _switch_language(message: Message, i18n: I18nContext, locale_code: str):
    await i18n.set_locale(locale_code)
    await message.answer(i18n.get("lang_is_switched"), reply_markup=main_kb())


async def _profile_message(
    message: Message,
    user_id: int,
    i18n: I18nContext,
    state: FSMContext,
    session: AsyncSession,
):
    await state.clear()
    user_data = await get_user_data(user_id, session)
    await message.answer(
        text=i18n.profile_message(
            telegram_id=message.from_user.id,
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
    await _profile_message(message, message.from_user.id, i18n, state, session)


@router.callback_query(F.data == "profile_button")
async def profile_callback(
    callback: CallbackQuery, i18n: I18nContext, state: FSMContext, session: AsyncSession
):
    await callback.message.delete()
    await _profile_message(
        callback.message, callback.from_user.id, i18n, state, session
    )


@router.callback_query(F.data == "language")
async def choose_language(callback: CallbackQuery, i18n: I18nContext):
    await callback.message.delete()
    await callback.message.answer(
        text=i18n.choose_language(), reply_markup=kb_language()
    )


@router.callback_query(F.data == "language_ru")
async def choose_language_ru(callback: CallbackQuery, i18n: I18nContext):
    await callback.message.delete()
    await _switch_language(callback.message, i18n, "ru")


@router.callback_query(F.data == "language_en")
async def choose_language_en(callback: CallbackQuery, i18n: I18nContext):
    await callback.message.delete()
    await _switch_language(callback.message, i18n, "en")


@router.callback_query(F.data == "email")
async def email(callback: CallbackQuery, i18n: I18nContext, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text=i18n.change_email(), reply_markup=back_to_profile()
    )
    await state.set_state(EmailState.change_email)


@router.message(EmailState.change_email)
async def change_email(
    message: Message, i18n: I18nContext, state: FSMContext, session: AsyncSession
):
    if not valid_email(message.text):
        await message.answer(text=i18n.not_valid_email())
    await update_email(message.from_user.id, message.text, session)
    await _profile_message(message, message.from_user.id, i18n, state, session)
