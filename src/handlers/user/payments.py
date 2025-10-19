from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from src.keyboards.payments_kb import kb_payment, kb_choose_method
from src.cruds.payment_crud import add_payment
from src.service.cryptopay import create_invoice_crypt
from src.service.yoomoney_api import create_invoice_yookassa

router = Router()


@router.callback_query(F.data == "pay")
async def choose_payment_method(
    callback: CallbackQuery, i18n: I18nContext, state: FSMContext
):
    await callback.message.delete()
    data = await state.get_data()
    await callback.message.answer(
        text=i18n.payment_method(name=data["name"]), reply_markup=kb_choose_method()
    )


@router.callback_query(F.data == "crypt")
async def crypt_method(
    callback: CallbackQuery, i18n: I18nContext, session: AsyncSession, state: FSMContext
):
    await callback.message.delete()
    data = await state.get_data()
    invoice = await create_invoice_crypt(
        data=data, user_id=callback.from_user.id, chat_id=callback.message.chat.id
    )
    await callback.message.answer(
        text=i18n.public_offer(
            name=data["name"],
            duration_days=data["duration_days"],
            price=data["price"],
            currency=data["currency"],
        ),
        reply_markup=kb_payment(invoice.bot_invoice_url),
    )
    await add_payment(
        user_id=callback.from_user.id,
        provider_payment_id=str(invoice.invoice_id),
        data=data,
        session=session,
    )


@router.callback_query(F.data == "yookassa")
async def yookassa_method(
    callback: CallbackQuery, i18n: I18nContext, session: AsyncSession, state: FSMContext
):
    await callback.message.delete()
    data = await state.get_data()
    invoice = create_invoice_yookassa(
        data=data, user_id=callback.from_user.id, chat_id=callback.message.chat.id
    )
    await callback.message.answer(
        text=i18n.public_offer(
            name=data["name"],
            duration_days=data["duration_days"],
            price=data["price"],
            currency=data["currency"],
        ),
        reply_markup=kb_payment(invoice.confirmation.confirmation_url),
    )
    await add_payment(
        user_id=callback.from_user.id,
        provider_payment_id=invoice.id,
        data=data,
        session=session,
    )
