from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram_i18n import I18nContext, LazyProxy
from aiogram.fsm.context import FSMContext

from keyboards.subscription_kb import kb_tariff, kb_payment
from src.cruds.subscription_crud import get_subscription
from src.service.utils import set_state

router = Router()


@router.message(F.text == LazyProxy("tariff_button"))
async def tariff(message: Message, i18n: I18nContext, session: AsyncSession):
    await message.answer(
        text=i18n.tariff_message(),
        reply_markup=await kb_tariff(session)
    )


@router.callback_query(F.data.startswith("subscription_"))
async def choose_subscription(
        callback: CallbackQuery,
        i18n: I18nContext,
        session: AsyncSession,
        state: FSMContext
):
    await callback.message.delete()
    name = callback.data.replace("subscription_", "")
    subscription_data = await get_subscription(name, session)
    await set_state(state, subscription_data)
    await callback.message.answer(
        text=i18n.subscription_message(
            name=subscription_data.name,
            duration_days=subscription_data.duration_days,
            price=subscription_data.price,
            currency=subscription_data.currency
        ),
        reply_markup=kb_payment()
    )
