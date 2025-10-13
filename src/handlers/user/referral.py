from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from service.utils import get_ref_link
from src.keyboards.referral_kb import referral, back_to_referral_info
from src.cruds.user_crud import get_referrals

router = Router()


@router.callback_query(F.data == "referral_info")
async def referral_info_handler(callback: CallbackQuery, i18n: I18nContext):
    await callback.message.answer(
        text=i18n.referral_info(),
        reply_markup=referral()
    )


@router.callback_query(F.data == "invite_friend")
async def invite_friend_command(callback: CallbackQuery, i18n: I18nContext):
    bot_username = callback.from_user.username
    user_id = callback.from_user.id
    ref_link = get_ref_link(bot_username, user_id)
    await callback.message.answer(
        text=i18n.invite_friend_message(ref_link=ref_link),
        reply_markup=back_to_referral_info()
    )


@router.callback_query(F.data == "my_referrals")
async def my_referrals(callback: CallbackQuery, i18n: I18nContext, session: AsyncSession):
    """Показывает пользователю список или статистику его рефералов."""
    user_id = callback.from_user.id
    referrals = get_referrals(user_id, session)
    if not referrals:
        text = i18n.not_referral()
    else:
        ref_list = i18n.referral_list()
        for u in referrals:
            uname = f"@{u.username}" if u.username else f"ID {u.id}"
            ref_list += f"• {uname}\n"
        ref_list += i18n.referral_all(len(referrals))
        text = ref_list
    await callback.message.edit_text(text, reply_markup=back_to_referral_info())
