from pydantic import BaseModel, Field


class SolarPlanningRequest(BaseModel):
    average_monthly_consumption_kwh: float | None = Field(
        default=None,
        gt=0,
    )

    system_capacity_kw: float = Field(
        gt=0,
        le=1000,
    )

    installation_cost_lkr: float | None = Field(
        default=None,
        gt=0,
    )

    import_tariff_lkr_per_kwh: float | None = Field(
        default=None,
        ge=0,
    )

    export_rate_lkr_per_kwh: float | None = Field(
        default=None,
        ge=0,
    )

    specific_yield_kwh_per_kw_year: float | None = Field(
        default=None,
        gt=0,
    )

    self_consumption_ratio: float = Field(
        default=0.40,
        ge=0,
        le=1,
    )


class SolarPlanningScenario(BaseModel):
    system_capacity_kw: float

    annual_consumption_kwh: float | None

    estimated_annual_generation_kwh: float | None

    self_consumed_solar_kwh: float | None

    exported_solar_kwh: float | None

    grid_import_kwh: float | None

    energy_coverage_percent: float | None

    avoided_import_cost_lkr: float | None

    export_income_lkr: float | None

    estimated_annual_benefit_lkr: float | None

    simple_payback_years: float | None

    calculation_ready: bool

    financial_calculation_ready: bool

    missing_inputs: list[str]

    assumptions: list[str]


class SolarScenarioComparisonRequest(BaseModel):
    average_monthly_consumption_kwh: float | None = Field(
        default=None,
        gt=0,
    )

    capacities_kw: list[float] = Field(
        min_length=1,
        max_length=10,
    )

    installation_costs_lkr: dict[str, float] | None = None

    import_tariff_lkr_per_kwh: float | None = Field(
        default=None,
        ge=0,
    )

    export_rate_lkr_per_kwh: float | None = Field(
        default=None,
        ge=0,
    )

    specific_yield_kwh_per_kw_year: float | None = Field(
        default=None,
        gt=0,
    )

    self_consumption_ratio: float = Field(
        default=0.40,
        ge=0,
        le=1,
    )


class SolarScenarioComparisonResponse(BaseModel):
    scenarios: list[SolarPlanningScenario]
