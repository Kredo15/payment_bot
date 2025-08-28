from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.core.settings import settings
from src.utils import check_admin


class IsSuperAdmin(BaseFilter):
    """
    Filter to check if the user is a super admin.

    Attributes:
        super_admin (int): The ID of the super admin.
    """

    def __init__(self):
        self.super_admin = settings.ADMIN

    async def __call__(self, message: Message) -> bool:
        """
        Checks if the message sender is the super admin.

        Args:
            message (Message): The message object from the user.

        Returns:
            bool: True if the user is the super admin, False otherwise.
        """
        user_id = message.from_user.id
        if user_id == self.super_admin:
            return True
        else:
            return False


class IsAdmin(BaseFilter):
    """
    Filter to check if the user is an admin or the super admin.

    Attributes:
        super_admin (int): The ID of the super admin.
    """

    def __init__(self):
        self.super_admin = settings.ADMIN

    async def __call__(self, message: Message) -> bool:
        """
        Checks if the message sender is an admin or the super admin.

        Args:
            message (Message): The message object from the user.

        Returns:
            bool: True if the user is an admin or the super admin, False otherwise.
        """
        self.user_id = message.from_user.id
        self.is_admin = await check_admin(user_id=self.user_id)
        if self.user_id == settings.ADMIN:
            return True
        elif self.is_admin:
            return True
        else:
            return False
