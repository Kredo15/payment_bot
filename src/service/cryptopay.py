import logging

from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update
from aiocryptopay.models.invoice import Invoice
from aiogram_i18n import LazyProxy

from src.core.settings import settings
from src.cruds.payment_crud import update_payment
from src.cruds.subscription_crud import add_history_subscription
from src.database.enums import StatusPaymentEnum
from src.core.app import bot
from src.keyboards.common_kb import kb_chanel
from src.core.message import LogMessages

logger = logging.getLogger(__name__)

crypto = AioCryptoPay(token=settings.crypto_settings.CRYPTO_PAY_TOKEN, network=Networks.TEST_NET)


@crypto.pay_handler()
async def handle_payment(update: Update, app):
    try:
        name_sub, user_id, chat_id = update.payload.payload.split("|")
    except Exception:  # noinspection PyBroadException
        logger.warning(LogMessages.INVALID_INVOICE.format(
            method="crypto", request=update.payload.payload
        ))
        return None
    if update.payload.status == 'paid':
        status = StatusPaymentEnum.completed
        end_data = await add_history_subscription(
            name_sub=name_sub,
            user_id=user_id,
            invoice_id=str(update.payload.invoice_id)
        )
        end_data = end_data.strftime("%d/%m/%Y, %H:%M:%S").split()
        text = LazyProxy("success_payment", end_data=end_data[0])
        markup = kb_chanel()
        logger.info(LogMessages.CREATE_INVOICE.format(
            user_id=user_id, name=name_sub, method="crypto"
        ))
    else:
        status = StatusPaymentEnum.failed
        text = LazyProxy("failed_payment")
        markup = None
        logger.info(LogMessages.FAILED_INVOICE.format(
            user_id=user_id, name=name_sub, method="crypto"
        ))
    await update_payment(str(update.payload.invoice_id), status)
    await bot.send_message(chat_id, text, reply_markup=markup)
    await bot.promote_chat_member(settings.PRIVATE_CHANEL, user_id)


async def create_invoice_crypt(data, user_id: int, chat_id: int) -> Invoice:
    invoice = await crypto.create_invoice(
        currency_type='fiat',
        fiat=data["currency"],
        accepted_assets=settings.crypto_settings.ACCEPTED_ASSETS,
        amount=data["price"],
        payload=f'{data["name"]} | {user_id} | {chat_id}'
    )
    logger.info(LogMessages.CREATE_INVOICE.format(
        user_id=user_id, name=data["name"], method="crypto"
    ))
    return invoice


async def close_session(app) -> None:
    await crypto.close()
