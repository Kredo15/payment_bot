import enum


class StatusPaymentEnum(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class StatusSubscriptionEnum(str, enum.Enum):
    active = "active"
    expired = "expired"
    cancelled = "cancelled"


class RoleEnum(str, enum.Enum):
    owner = "owner"
    admin = "admin"
    moderator = "moderator"
