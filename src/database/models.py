from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    BigInteger,
    ForeignKey,
    String
)
from sqlalchemy.types import JSON, DECIMAL

from src.database.base_model import Base, intpk, created_at
from src.database.enums import (
    StatusPaymentEnum,
    StatusSubscriptionEnum,
    RoleEnum
)


class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    subscription_end_date: Mapped[datetime | None]
    is_active: Mapped[bool] = mapped_column(default=False)


class Payments(Base):
    __tablename__ = "payments"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE")
    )
    amount: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    currency: Mapped[str] = mapped_column(String(10), default='RUB')
    provider_payment_id: Mapped[str] = mapped_column(unique=True)
    status: Mapped[StatusPaymentEnum] = mapped_column(default=StatusPaymentEnum.pending)
    subscription_period: Mapped[int]
    created_at: Mapped[created_at]


class Subscriptions(Base):
    __tablename__ = "subscriptions"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    currency: Mapped[str] = mapped_column(String(10), default='RUB')
    duration_days: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[datetime | None]


class SubscriptionHistory(Base):
    __tablename__ = "subscription_history"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("subscriptions.id", ondelete="CASCADE")
    )
    payment_id: Mapped[int] = mapped_column(
        ForeignKey("payments.id", ondelete="CASCADE")
    )
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    status: Mapped[StatusSubscriptionEnum] = mapped_column(
        default=StatusSubscriptionEnum.active
    )
    created_at: Mapped[created_at]


class Admins(Base):
    __tablename__ = "admins"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    role: Mapped[RoleEnum]
    created_at: Mapped[created_at]


class ActivityLogs(Base):
    __tablename__ = "activity_logs"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    action: Mapped[str]
    details: Mapped[str] = mapped_column(type_=JSON)
    created_at: Mapped[created_at]
