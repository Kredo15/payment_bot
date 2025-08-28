from aiogram_i18n.managers import BaseManager
from aiogram.types.user import User
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import get_language, set_language


class UserManager(BaseManager):
    async def get_locale(
            self,
            event_from_user: User
    ) -> str:
        default = event_from_user.language_code or self.default_locale
        user_lang = await get_language(event_from_user.id)
        if user_lang:
            return user_lang
        return default

    async def set_locale(
            self,
            locale: str,
            event_from_user: User
    ) -> None:
        await set_language(event_from_user.id, locale)
