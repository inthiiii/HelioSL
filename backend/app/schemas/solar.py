from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SolarSystemCreate(BaseModel):
    capacity_kw: Decimal = Field(
        gt=0,
        le=1000,
    )

    installation_date: date | None = None
    scheme: str | None = None
    panel_brand: str | None = None
    inverter_brand: str | None = None
    installer_name: str | None = None


class SolarSystemResponse(
    SolarSystemCreate
):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class SolarGenerationCreate(BaseModel):
    generation_month: date

    generation_kwh: Decimal = Field(
        ge=0,
    )

    exported_kwh: Decimal | None = Field(
        default=None,
        ge=0,
    )

    imported_kwh: Decimal | None = Field(
        default=None,
        ge=0,
    )


class SolarGenerationResponse(
    SolarGenerationCreate
):
    id: int
    solar_system_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )