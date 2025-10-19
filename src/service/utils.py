import logging

from src.core.state import PaymentState

logger = logging.getLogger(__name__)


async def set_state(state, subscription_data):
    await state.clear()
    await state.set_state(PaymentState.subscription)
    data = await state.get_data()
    data["name"] = subscription_data.name
    data["duration_days"] = subscription_data.duration_days
    data["price"] = float(subscription_data.price)
    data["currency"] = subscription_data.currency
    await state.update_data(data)


def get_ref_link(bot_username: str, user_id: int) -> str:
    """
    Генерирует персональную реферальную ссылку для пользователя.
    """
    return f"https://t.me/{bot_username}?start=ref_{user_id}"


def get_referral(message) -> None | int:
    user_id = message.from_user.id
    args = message.get_args() if hasattr(message, "get_args") else ""
    if not args and message.text:
        parts = message.text.split(maxsplit=1)
        if len(parts) == 2:
            args = parts[1]

    # Парсим referrer_id из args
    if args and args.startswith("ref_"):
        try:
            ref_id = int(args[4:])
            if ref_id != user_id:
                return ref_id
        except Exception:
            pass
    return None
