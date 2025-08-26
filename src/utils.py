from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import AdminsOrm, UsersOrm


async def check_admin(user_id: int, session: AsyncSession) -> bool:
    admins = await session.scalar(select(AdminsOrm).join(UsersOrm).where(UsersOrm.is_active))
    if admins:
        admins = [admin.telegram_id for admin in admins.all()]
        return user_id in admins
    return False
