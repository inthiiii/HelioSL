from typing import Any

from pydantic import BaseModel


class IntegratedSummary(BaseModel):
    user_type: str
    district: str | None

    energy_profile_available: bool
    solar_system_available: bool

    energy: dict[str, Any]
    solar: dict[str, Any]

    alerts: list[str]
