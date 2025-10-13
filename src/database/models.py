from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    ForeignKey,
    String
)
from sqlalchemy.types import JSON, DECIMAL
from pydantic import EmailStr

from src.database.base_model import Base, intpk, created_at
from src.database.enums import (
    StatusPaymentEnum,
    StatusSubscriptionEnum,
    RoleEnum
)


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    email: Mapped[EmailStr] = mapped_column(
        String, nullable=True
    )
    language: Mapped[str] = mapped_column(default='ru')
    subscription_end_date: Mapped[datetime | None]
    is_active: Mapped[bool] = mapped_column(default=True)

    payment: Mapped[list["PaymentsOrm"]] = relationship(
       back_populates='user', cascade='all, delete-orphan'
    )
    history: Mapped[list["SubscriptionHistoryOrm"]] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    admin: Mapped[list["AdminsOrm"]] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    logs: Mapped[list["ActivityLogsOrm"]] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )


class PaymentsOrm(Base):
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

    user: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="payment")
    history: Mapped[list["SubscriptionHistoryOrm"]] = relationship(
        back_populates='payment', cascade='all, delete-orphan'
    )


class SubscriptionsOrm(Base):
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

    history: Mapped[list["SubscriptionHistoryOrm"]] = relationship(
        back_populates='subscription', cascade='all, delete-orphan'
    )


class SubscriptionHistoryOrm(Base):
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

    user: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="history")
    subscription: Mapped["SubscriptionsOrm"] = relationship("SubscriptionsOrm", back_populates="history")
    payment: Mapped["PaymentsOrm"] = relationship("PaymentsOrm", back_populates="history")


class AdminsOrm(Base):
    __tablename__ = "admins"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    role: Mapped[RoleEnum]
    created_at: Mapped[created_at]

    user: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="admin")


class ActivityLogsOrm(Base):
    __tablename__ = "activity_logs"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    action: Mapped[str]
    details: Mapped[str] = mapped_column(type_=JSON)
    created_at: Mapped[created_at]

    user: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="logs")
