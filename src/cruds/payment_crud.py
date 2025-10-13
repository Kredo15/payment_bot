from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import PaymentsOrm
from src.database.enums import StatusPaymentEnum
from src.core.db_dependency import get_async_session


async def add_payment(
        user_id: int,
        provider_payment_id: str,
        data: dict,
        session: AsyncSession
) -> None:
    values = {
        "user_id": user_id,
        "amount": data["price"],
        "currency": data["currency"],
        "provider_payment_id": provider_payment_id
    }
    await session.execute(
        insert(PaymentsOrm).values(values)
    )
    await session.commit()


async def update_payment(
        payment_id: str,
        status: StatusPaymentEnum
) -> None:
    async with get_async_session() as session:
        await session.scalar(update(PaymentsOrm).where(
            PaymentsOrm.provider_payment_id == payment_id
            ).values(status=status)
        )
        await session.commit()
