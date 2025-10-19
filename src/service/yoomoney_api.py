import uuid
from aiohttp.web_request import Request
import logging

from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotification
from aiogram_i18n import LazyProxy

from src.core.settings import settings
from src.cruds.subscription_crud import add_history_subscription
from src.database.enums import StatusPaymentEnum
from src.cruds.payment_crud import update_payment
from src.core.app import bot
from src.keyboards.common_kb import kb_chanel
from src.core.message import LogMessages

logger = logging.getLogger(__name__)

Configuration.account_id = settings.yoomoney_settings.YOOMONEY_ACCOUNT_ID
Configuration.secret_key = settings.yoomoney_settings.YOOMONEY_SECRET_KEY


def create_invoice_yookassa(data: dict, user_id: int, chat_id: int):
    id_key = str(uuid.uuid4())
    invoice = Payment.create(
        {
            "amount": {"value": data["price"], "currency": data["currency"]},
            "payment_method_data": {"type": "bank_card"},
            "confirmation": {
                "type": "redirect",
                "return_url": settings.yoomoney_settings.YOOMONEY_REDIRECT_URL,
            },
            "capture": True,
            "metadata": {
                "user_id": user_id,
                "chat_id": chat_id,
                "name_sub": data["name"],
            },
            "description": "Подписка на закрытый канал",
        },
        id_key,
    )

    return invoice


def parse_webhook_notification(request_body: dict) -> WebhookNotification | None:
    """Пытается распарсить webhook Yookassa; при ошибке возвращает None."""
    try:
        notification_object = WebhookNotification(request_body)
        return notification_object
    except Exception:  # noinspection PyBroadException
        return None


async def yookassa_webhook_handler(request: Request):
    try:
        body = await request.json()
    except Exception:  # noinspection PyBroadException
        logger.warning(LogMessages.INVALID_JSON.format(request=request))
        return None
    notification = parse_webhook_notification(body)
    if not notification:
        logger.warning(
            LogMessages.INVALID_INVOICE.format(method="yookassa", request=body)
        )
        return None
    meta = getattr(notification.object, "metadata", None) or {}
    user_id = int(meta["user_id"])
    chat_id = int(meta["chat_id"])
    name_sub = meta["name_sub"]
    if notification.event == "payment.succeeded":
        status = StatusPaymentEnum.completed
        end_data = await add_history_subscription(
            name_sub=name_sub, user_id=user_id, invoice_id=notification.object.id
        )
        end_data = end_data.strftime("%d/%m/%Y, %H:%M:%S").split()
        text = LazyProxy("success_payment", end_data=end_data[0])
        markup = kb_chanel()
        logger.info(
            LogMessages.CREATE_INVOICE.format(
                user_id=user_id, name=name_sub, method="yookassa"
            )
        )
    else:
        status = StatusPaymentEnum.failed
        text = LazyProxy("failed_payment")
        markup = None
        logger.info(
            LogMessages.FAILED_INVOICE.format(
                user_id=user_id, name=name_sub, method="yookassa"
            )
        )
    await update_payment(notification.object.id, status)
    await bot.send_message(chat_id, text, reply_markup=markup)
    await bot.promote_chat_member(settings.PRIVATE_CHANEL, user_id)
