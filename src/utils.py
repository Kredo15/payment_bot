import logging

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import AdminsOrm, UsersOrm, SubscriptionsOrm
from src.core.db_dependency import get_async_session

logger = logging.getLogger(__name__)


async def check_admin(user_id: int) -> bool:
    async with get_async_session() as session:
        admins = await session.scalar(select(AdminsOrm).join(UsersOrm).where(UsersOrm.is_active))
        if admins:
            admins = [admin.telegram_id for admin in admins.all()]
            return user_id in admins
    return False


async def check_user(user_id: int, session: AsyncSession):
    user = await session.scalar(
        select(UsersOrm).where(UsersOrm.telegram_id == user_id)
    )
    if not user:
        await session.execute(
            insert(UsersOrm).values(telegram_id=user_id)
        )


async def get_user_data(user_id: int, session: AsyncSession) -> str:
    pass


async def get_language(user_id: int) -> str | None:
    # noinspection PyBroadException
    try:
        async with get_async_session() as session:
            lang = await session.scalar(
                select(UsersOrm).where(UsersOrm.telegram_id == user_id)
            )
        return lang.language
    except Exception as e:
        logger.warning('user not found')
        return None


async def set_language(user_id: int, locale: str) -> None:
    async with get_async_session() as session:
        await session.execute(
            update(UsersOrm).where(UsersOrm.telegram_id == user_id)
            .values(language=locale)
        )


async def get_subscriptions(session: AsyncSession):
    subscriptions = await session.scalars(
        select(SubscriptionsOrm).where(SubscriptionsOrm.is_active)
        .order_by(SubscriptionsOrm.duration_days)
    )
    return subscriptions.all()
