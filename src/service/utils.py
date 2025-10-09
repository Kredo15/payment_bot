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
