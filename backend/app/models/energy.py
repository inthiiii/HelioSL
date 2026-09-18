from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EnergyProfile(Base):
    __tablename__ = "energy_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    provider: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    connection_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    average_monthly_consumption_kwh: Mapped[
        Decimal | None
    ] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    average_monthly_bill_lkr: Mapped[
        Decimal | None
    ] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="energy_profile",
    )


class ConsumptionRecord(Base):
    __tablename__ = "consumption_records"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "billing_month",
            name="uq_consumption_user_month",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    billing_month: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    consumption_kwh: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    bill_amount_lkr: Mapped[
        Decimal | None
    ] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="consumption_records",
    )