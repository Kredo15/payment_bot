from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import SubscriptionsOrm


async def create_test_subscriptions(
        async_session: AsyncSession
):
    async with async_session:
        await async_session.execute(
            insert(SubscriptionsOrm).values(
                [
                    {
                        "name": "30 дней",
                        "price": 100,
                        "currency": "RUB",
                        "duration_days": 30
                    },
                    {
                        "name": "90 дней",
                        "price": 250,
                        "currency": "RUB",
                        "duration_days": 90
                    }
                ]
            )
        )
        await async_session.commit()
