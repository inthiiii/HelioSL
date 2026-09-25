from pydantic import BaseModel

class EnergyIntelligenceSummary(BaseModel):
    average_consumption_kwh: float | None
    latest_consumption_kwh: float | None
    consumption_change_percent: float | None

    average_generation_kwh: float | None
    latest_generation_kwh: float | None
    generation_change_percent: float | None

    consumption_trend: str
    generation_trend: str

    generation_anomaly: bool