from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram_i18n import I18nContext, LazyProxy

from src.app import bot
from src.keyboards.users_kb import kb_tariff
from src.utils import get_user_data, check_user
from src.keyboards.users_kb import (
    main_kb,
    kb_profile,
    kb_language
)

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext, session: AsyncSession):
    await check_user(message.from_user.id, session)
    name = message.from_user.full_name
    await message.answer(
        text=i18n.hello(user=name),
        reply_markup=main_kb()
    )


@router.message(F.text == LazyProxy("tariff_button"))
async def tariff(message: Message, i18n: I18nContext, session: AsyncSession):
    await message.answer(
        text=i18n.tariff_message(),
        reply_markup=await kb_tariff(session)
    )


@router.message(F.text == LazyProxy("profile_button"))
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


@router.message(F.text == LazyProxy("support_button"))
async def support(message: Message, i18n: I18nContext):
    await message.answer(
        text=i18n.support_message()
    )


async def _switch_language(message: Message, i18n: I18nContext, locale_code: str):
    await i18n.set_locale(locale_code)
    await message.answer(
        i18n.get("lang_is_switched"),
        reply_markup=await main_kb()
    )


@router.callback_query(F.data == "language")
async def choose_language(callback: CallbackQuery, i18n: I18nContext):
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await callback.message.answer(
        text=i18n.choose_language(),
        reply_markup=kb_language()
    )


@router.callback_query(F.data == "language_ru")
async def choose_language(callback: CallbackQuery, i18n: I18nContext):
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await _switch_language(callback.message, i18n, "ru")


@router.callback_query(F.data == "language_en")
async def choose_language(callback: CallbackQuery, i18n: I18nContext):
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await _switch_language(callback.message, i18n, "en")
