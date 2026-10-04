from app.schemas.planning import (
    SolarPlanningRequest,
)
from app.services.analytics_service import (
    percentage_change,
    trend_from_change,
)
from app.services.planning_service import (
    calculate_solar_scenario,
)
from scripts.seed_space_industries import (
    SPACE_INDUSTRIES_CONSUMPTION,
    SPACE_INDUSTRIES_GENERATION,
)


def test_household_demo_planning():
    request = SolarPlanningRequest(
        system_capacity_kw=5,
        installation_cost_lkr=1_250_000,
        import_tariff_lkr_per_kwh=50,
        export_rate_lkr_per_kwh=27,
        specific_yield_kwh_per_kw_year=1400,
        self_consumption_ratio=0.40,
    )

    result = calculate_solar_scenario(
        average_monthly_consumption_kwh=453.67,
        data=request,
    )

    assert result.calculation_ready is True
    assert result.financial_calculation_ready is True
    assert result.annual_consumption_kwh == 5444.04
    assert result.estimated_annual_generation_kwh == 7000
    assert result.self_consumed_solar_kwh == 2800
    assert result.exported_solar_kwh == 4200
    assert result.grid_import_kwh == 2644.04
    assert result.simple_payback_years is not None


def test_business_demo_planning():
    request = SolarPlanningRequest(
        system_capacity_kw=20,
        installation_cost_lkr=4_200_000,
        import_tariff_lkr_per_kwh=55,
        export_rate_lkr_per_kwh=27,
        specific_yield_kwh_per_kw_year=1400,
        self_consumption_ratio=0.70,
    )

    result = calculate_solar_scenario(
        average_monthly_consumption_kwh=2114.44,
        data=request,
    )

    assert result.calculation_ready is True
    assert result.financial_calculation_ready is True
    assert result.annual_consumption_kwh == 25373.28
    assert result.estimated_annual_generation_kwh == 28000
    assert result.self_consumed_solar_kwh == 19600
    assert result.exported_solar_kwh == 8400
    assert result.grid_import_kwh == 5773.28
    assert result.energy_coverage_percent is not None
    assert result.simple_payback_years is not None


def test_household_consumption_is_increasing():
    change = percentage_change(
        482,
        495,
    )

    assert change is not None
    assert change > 0
    assert change == 2.7


def test_household_generation_is_decreasing():
    change = percentage_change(
        525,
        475,
    )

    assert change is not None
    assert change < 0
    assert change == -9.52
    assert trend_from_change(change) == "decreasing"


def test_business_demo_trends_match_seeded_records():
    consumption_change = percentage_change(
        2310,
        2390,
    )
    generation_change = percentage_change(
        2110,
        1950,
    )

    assert consumption_change == 3.46
    assert generation_change == -7.58
    assert trend_from_change(
        generation_change
    ) == "decreasing"


def test_space_industries_has_more_than_one_year_of_data():
    assert len(SPACE_INDUSTRIES_CONSUMPTION) == 18
    assert len(SPACE_INDUSTRIES_GENERATION) == 18

    first_consumption_month = (
        SPACE_INDUSTRIES_CONSUMPTION[0][0]
    )
    last_consumption_month = (
        SPACE_INDUSTRIES_CONSUMPTION[-1][0]
    )

    assert first_consumption_month == "2025-04-01"
    assert last_consumption_month == "2026-09-01"
