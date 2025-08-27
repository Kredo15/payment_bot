from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import AdminsOrm, UsersOrm


async def check_admin(user_id: int, session: AsyncSession) -> bool:
    admins = await session.scalar(select(AdminsOrm).join(UsersOrm).where(UsersOrm.is_active))
    if admins:
        admins = [admin.telegram_id for admin in admins.all()]
        return user_id in admins
    return False


async def get_user_data(user_id: int, session: AsyncSession) -> str:
    pass


async def get_language(user_id: int, session: AsyncSession) -> str:
    lang = await session.scalar(
        select(UsersOrm).where(UsersOrm.telegram_id == user_id)
    )
    return lang.language


async def set_language(user_id: int, locale: str, session: AsyncSession) -> None:
    await session.scalar(
        update(UsersOrm).where(UsersOrm.telegram_id == user_id)
        .values(language=locale)
    )
