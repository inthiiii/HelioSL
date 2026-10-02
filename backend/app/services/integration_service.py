from sqlalchemy.orm import Session

from app.models.user import User
from app.services.analytics_service import (
    analyze_energy_data,
)
from app.services.energy_service import (
    get_consumption_records,
    get_energy_profile,
)
from app.services.solar_service import (
    get_generation_records,
    get_solar_system,
)


def build_integrated_summary(
    db: Session,
    user: User,
) -> dict:
    profile = get_energy_profile(
        db,
        user.id,
    )

    consumption = get_consumption_records(
        db,
        user.id,
    )

    solar = get_solar_system(
        db,
        user.id,
    )

    generation = []

    if solar:
        generation = get_generation_records(
            db,
            solar.id,
        )

    analytics = analyze_energy_data(
        consumption,
        generation,
    )

    alerts: list[str] = []

    if (
        analytics.get(
            "consumption_trend"
        )
        == "increasing"
    ):
        alerts.append(
            "Electricity consumption is increasing."
        )

    if (
        analytics.get(
            "generation_trend"
        )
        == "decreasing"
    ):
        alerts.append(
            "Solar generation is decreasing."
        )

    if analytics.get(
        "generation_anomaly"
    ):
        alerts.append(
            "Solar generation may be below "
            "the historical baseline."
        )

    energy_data = {
        "provider": (
            profile.provider
            if profile
            else None
        ),
        "connection_type": (
            profile.connection_type
            if profile
            else None
        ),
        "profile_average_consumption_kwh": (
            float(
                profile.average_monthly_consumption_kwh
            )
            if profile
            and profile.average_monthly_consumption_kwh
            is not None
            else None
        ),
        **analytics,
    }

    solar_data = {
        "capacity_kw": (
            float(
                solar.capacity_kw
            )
            if solar
            else None
        ),
        "scheme": (
            solar.scheme
            if solar
            else None
        ),
        "installation_date": (
            str(
                solar.installation_date
            )
            if solar
            and solar.installation_date
            else None
        ),
        "record_count": len(generation),
    }

    return {
        "user_type": user.user_type,
        "district": user.district,
        "energy_profile_available": (
            profile is not None
        ),
        "solar_system_available": (
            solar is not None
        ),
        "energy": energy_data,
        "solar": solar_data,
        "alerts": alerts,
    }
