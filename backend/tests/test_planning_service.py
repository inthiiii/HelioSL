from app.schemas.planning import (
    SolarPlanningRequest,
)
from app.services.planning_service import (
    calculate_solar_scenario,
)


def test_complete_financial_scenario():

    request = SolarPlanningRequest(
        system_capacity_kw=5,
        installation_cost_lkr=1_200_000,
        import_tariff_lkr_per_kwh=50,
        export_rate_lkr_per_kwh=27,
        specific_yield_kwh_per_kw_year=1400,
        self_consumption_ratio=0.4,
    )

    result = calculate_solar_scenario(
        average_monthly_consumption_kwh=450,
        data=request,
    )

    assert result.annual_consumption_kwh == 5400

    assert (
        result.estimated_annual_generation_kwh
        == 7000
    )

    assert result.calculation_ready is True

    assert (
        result.financial_calculation_ready
        is True
    )

    assert result.simple_payback_years is not None
    assert result.self_consumed_solar_kwh == 2800
    assert result.exported_solar_kwh == 4200
    assert result.avoided_import_cost_lkr == 140000
    assert result.export_income_lkr == 113400
    assert result.estimated_annual_benefit_lkr == 253400
    assert result.simple_payback_years == 4.74
    assert result.missing_inputs == []


def test_missing_tariff_does_not_invent_financial_result():

    request = SolarPlanningRequest(
        system_capacity_kw=5,
        specific_yield_kwh_per_kw_year=1400,
    )

    result = calculate_solar_scenario(
        average_monthly_consumption_kwh=450,
        data=request,
    )

    assert result.calculation_ready is True

    assert (
        result.financial_calculation_ready
        is False
    )

    assert (
        result.simple_payback_years
        is None
    )

    assert result.estimated_annual_benefit_lkr is None
    assert "import_tariff_lkr_per_kwh" in result.missing_inputs
    assert "export_rate_lkr_per_kwh" in result.missing_inputs


def test_missing_solar_yield_reports_incomplete_calculation():
    request = SolarPlanningRequest(
        system_capacity_kw=5,
        installation_cost_lkr=1_200_000,
        import_tariff_lkr_per_kwh=50,
        export_rate_lkr_per_kwh=27,
    )

    result = calculate_solar_scenario(
        average_monthly_consumption_kwh=450,
        data=request,
    )

    assert result.calculation_ready is False
    assert result.estimated_annual_generation_kwh is None
    assert result.energy_coverage_percent is None
    assert result.financial_calculation_ready is False
    assert result.missing_inputs == [
        "specific_yield_kwh_per_kw_year",
    ]


def test_missing_consumption_blocks_energy_analysis():

    request = SolarPlanningRequest(
        system_capacity_kw=5,
        specific_yield_kwh_per_kw_year=1400,
    )

    result = calculate_solar_scenario(
        average_monthly_consumption_kwh=None,
        data=request,
    )

    assert result.calculation_ready is False

    assert (
        "average_monthly_consumption_kwh"
        in result.missing_inputs
    )
