from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from src.keyboards.users_kb import main_kb
from src.keyboards.profile_kb import kb_language

router = Router()


async def _switch_language(message: Message, i18n: I18nContext, locale_code: str):
    await i18n.set_locale(locale_code)
    await message.answer(i18n.get("lang_is_switched"), reply_markup=main_kb())


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
