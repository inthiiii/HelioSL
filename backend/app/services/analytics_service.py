from app.models.energy import ConsumptionRecord
from app.models.solar import SolarGenerationRecord


def percentage_change(
    previous: float,
    current: float,
) -> float | None:
    if previous == 0:
        return None

    return round(
        ((current - previous) / previous) * 100,
        2,
    )


def trend_from_change(
    change: float | None,
) -> str:
    if change is None:
        return "insufficient_data"

    if change > 5:
        return "increasing"

    if change < -5:
        return "decreasing"

    return "stable"


def analyze_energy_data(
    consumption_records: list[ConsumptionRecord],
    generation_records: list[SolarGenerationRecord],
):
    consumption_values = [
        float(record.consumption_kwh)
        for record in consumption_records
    ]

    generation_values = [
        float(record.generation_kwh)
        for record in generation_records
    ]

    average_consumption = (
        round(
            sum(consumption_values)
            / len(consumption_values),
            2,
        )
        if consumption_values
        else None
    )

    average_generation = (
        round(
            sum(generation_values)
            / len(generation_values),
            2,
        )
        if generation_values
        else None
    )

    consumption_change = None

    if len(consumption_values) >= 2:
        consumption_change = percentage_change(
            consumption_values[-2],
            consumption_values[-1],
        )

    generation_change = None

    if len(generation_values) >= 2:
        generation_change = percentage_change(
            generation_values[-2],
            generation_values[-1],
        )

    generation_anomaly = False

    if (
        average_generation
        and generation_values
    ):
        latest_generation = generation_values[-1]

        generation_anomaly = (
            latest_generation
            < average_generation * 0.8
        )

    return {
        "average_consumption_kwh":
            average_consumption,

        "latest_consumption_kwh":
            consumption_values[-1]
            if consumption_values
            else None,

        "consumption_change_percent":
            consumption_change,

        "average_generation_kwh":
            average_generation,

        "latest_generation_kwh":
            generation_values[-1]
            if generation_values
            else None,

        "generation_change_percent":
            generation_change,

        "consumption_trend":
            trend_from_change(
                consumption_change
            ),

        "generation_trend":
            trend_from_change(
                generation_change
            ),

        "generation_anomaly":
            generation_anomaly,
    }