from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class BillExtractionResponse(BaseModel):
    filename: str
    provider: str | None
    account_number: str | None
    billing_month: date | None
    consumption_kwh: Decimal | None = Field(
        default=None,
        ge=0,
    )
    bill_amount_lkr: Decimal | None = Field(
        default=None,
        ge=0,
    )
    previous_meter_reading: Decimal | None = Field(
        default=None,
        ge=0,
    )
    current_meter_reading: Decimal | None = Field(
        default=None,
        ge=0,
    )
    confidence: str
    confidence_score: float = Field(
        ge=0,
        le=1,
    )
    warnings: list[str]
