import logging

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import Sequence

from src.database.models import AdminsOrm, UsersOrm
from src.core.db_dependency import get_async_session

logger = logging.getLogger(__name__)


async def check_admin(user_id: int) -> bool:
    async with get_async_session() as session:
        admins = await session.scalar(select(AdminsOrm).join(UsersOrm).where(UsersOrm.is_active))
        if admins:
            admins = [admin.telegram_id for admin in admins.all()]
            return user_id in admins
    return False


async def check_user(
        user_id: int,
        first_name: str,
        username: str,
        referral_id: int,
        session: AsyncSession):
    user = await session.scalar(
        select(UsersOrm).where(UsersOrm.telegram_id == user_id)
    )
    if not user:
        await session.execute(
            insert(UsersOrm).values(
                telegram_id=user_id,
                username=username,
                first_name=first_name,
                referral_id=referral_id
            )
        )
        await session.commit()


async def get_user_data(user_id: int, session: AsyncSession) -> dict:
    user = await session.scalar(
        select(UsersOrm).where(UsersOrm.telegram_id == user_id)
    )
    return {
        "email": user.email,
        "language": user.language,
    }


async def get_language(user_id: int) -> str | None:
    # noinspection PyBroadException
    try:
        async with get_async_session() as session:
            lang = await session.scalar(
                select(UsersOrm).where(UsersOrm.telegram_id == user_id)
            )
        return lang.language
    except Exception:
        logger.warning('user not found')
        return None


async def set_language(user_id: int, locale: str) -> None:
    async with get_async_session() as session:
        await session.execute(
            update(UsersOrm).where(UsersOrm.telegram_id == user_id)
            .values(language=locale)
        )
        await session.commit()


async def get_referrals(user_id: int, session: AsyncSession) -> Sequence:
    result = await session.scalars(select(UsersOrm).where(UsersOrm.referrer_id == user_id))
    return result.all()
