from sqlalchemy import select

from src.core.db_dependency import get_async_session
from src.database.models import AdminsOrm, UsersOrm


async def get_admins():
    async with get_async_session() as session:
        admins = await session.scalar(select(AdminsOrm).join(UsersOrm).where(UsersOrm.is_active))
    if admins:
        return [admin.telegram_id for admin in admins.all()]
    else:
        return []
