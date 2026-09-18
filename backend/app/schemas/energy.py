from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class EnergyProfileCreate(BaseModel):
    provider: str | None = None
    connection_type: str | None = None

    average_monthly_consumption_kwh: Decimal | None = Field(
        default=None,
        ge=0,
    )

    average_monthly_bill_lkr: Decimal | None = Field(
        default=None,
        ge=0,
    )


class EnergyProfileResponse(
    EnergyProfileCreate
):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class ConsumptionCreate(BaseModel):
    billing_month: date

    consumption_kwh: Decimal = Field(
        gt=0,
    )

    bill_amount_lkr: Decimal | None = Field(
        default=None,
        ge=0,
    )


class ConsumptionResponse(
    ConsumptionCreate
):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )