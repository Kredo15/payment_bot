from datetime import datetime, timedelta

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import Sequence

from src.database.models import SubscriptionsOrm, SubscriptionHistoryOrm, PaymentsOrm
from src.core.db_dependency import get_async_session


async def get_subscriptions(session: AsyncSession) -> Sequence:
    subscriptions = await session.scalars(
        select(SubscriptionsOrm)
        .where(SubscriptionsOrm.is_active)
        .order_by(SubscriptionsOrm.duration_days)
    )
    return subscriptions.all()


async def get_subscription(name: str, session: AsyncSession):
    subscription = await session.scalar(
        select(SubscriptionsOrm).where(
            SubscriptionsOrm.is_active, SubscriptionsOrm.name == name
        )
    )
    return subscription


async def add_history_subscription(
    name_sub: str, user_id: int, invoice_id: str
) -> datetime:
    async with get_async_session() as session:
        sub = await session.scalar(
            select(SubscriptionsOrm).where(
                SubscriptionsOrm.is_active, SubscriptionsOrm.name == name_sub
            )
        )
        payment = await session.scalar(
            select(PaymentsOrm).where(PaymentsOrm.provider_payment_id == invoice_id)
        )
        start_date = datetime.now()
        end_date = start_date + timedelta(days=sub.duration_days, minutes=15)
        await session.execute(
            insert(SubscriptionHistoryOrm).values(
                user_id=user_id,
                subscription=sub,
                payment=payment,
                start_date=start_date,
                end_date=end_date,
            )
        )
        await session.commit()
    return end_date
