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


class SolarSystem(Base):
    __tablename__ = "solar_systems"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    capacity_kw: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False,
    )

    installation_date: Mapped[
        date | None
    ] = mapped_column(
        Date,
        nullable=True,
    )

    scheme: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    panel_brand: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    inverter_brand: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    installer_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="solar_system",
    )

    generation_records = relationship(
        "SolarGenerationRecord",
        back_populates="solar_system",
        cascade="all, delete-orphan",
    )


class SolarGenerationRecord(Base):
    __tablename__ = "solar_generation_records"

    __table_args__ = (
        UniqueConstraint(
            "solar_system_id",
            "generation_month",
            name="uq_solar_generation_month",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    solar_system_id: Mapped[int] = mapped_column(
        ForeignKey(
            "solar_systems.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    generation_month: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    generation_kwh: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    exported_kwh: Mapped[
        Decimal | None
    ] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    imported_kwh: Mapped[
        Decimal | None
    ] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    solar_system = relationship(
        "SolarSystem",
        back_populates="generation_records",
    )