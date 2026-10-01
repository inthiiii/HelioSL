from app.schemas.planning import (
    SolarPlanningRequest,
    SolarPlanningScenario,
)


def calculate_solar_scenario(
    average_monthly_consumption_kwh: float | None,
    data: SolarPlanningRequest,
) -> SolarPlanningScenario:

    missing_inputs: list[str] = []
    assumptions: list[str] = []

    annual_consumption = None

    if average_monthly_consumption_kwh is not None:
        annual_consumption = round(
            average_monthly_consumption_kwh * 12,
            2,
        )
    else:
        missing_inputs.append(
            "average_monthly_consumption_kwh"
        )

    generation = None

    if data.specific_yield_kwh_per_kw_year is not None:
        generation = round(
            data.system_capacity_kw
            * data.specific_yield_kwh_per_kw_year,
            2,
        )

        assumptions.append(
            "Estimated solar generation uses the "
            "provided specific annual solar yield."
        )
    else:
        missing_inputs.append(
            "specific_yield_kwh_per_kw_year"
        )

    self_consumed = None
    exported = None
    grid_import = None
    coverage = None

    if (
        annual_consumption is not None
        and generation is not None
    ):
        potential_self_consumption = (
            generation
            * data.self_consumption_ratio
        )

        self_consumed = round(
            min(
                potential_self_consumption,
                annual_consumption,
            ),
            2,
        )

        exported = round(
            max(
                generation - self_consumed,
                0,
            ),
            2,
        )

        grid_import = round(
            max(
                annual_consumption
                - self_consumed,
                0,
            ),
            2,
        )

        coverage = round(
            (
                self_consumed
                / annual_consumption
                * 100
            )
            if annual_consumption > 0
            else 0,
            2,
        )

        assumptions.append(
            f"Self-consumption ratio assumed as "
            f"{data.self_consumption_ratio * 100:.0f}%."
        )

    avoided_cost = None

    if (
        self_consumed is not None
        and data.import_tariff_lkr_per_kwh
        is not None
    ):
        avoided_cost = round(
            self_consumed
            * data.import_tariff_lkr_per_kwh,
            2,
        )

    elif data.import_tariff_lkr_per_kwh is None:
        missing_inputs.append(
            "import_tariff_lkr_per_kwh"
        )

    export_income = None

    if (
        exported is not None
        and data.export_rate_lkr_per_kwh
        is not None
    ):
        export_income = round(
            exported
            * data.export_rate_lkr_per_kwh,
            2,
        )

    elif data.export_rate_lkr_per_kwh is None:
        missing_inputs.append(
            "export_rate_lkr_per_kwh"
        )

    annual_benefit = None

    if (
        avoided_cost is not None
        and export_income is not None
    ):
        annual_benefit = round(
            avoided_cost
            + export_income,
            2,
        )

    payback = None

    if (
        annual_benefit is not None
        and annual_benefit > 0
        and data.installation_cost_lkr
        is not None
    ):
        payback = round(
            data.installation_cost_lkr
            / annual_benefit,
            2,
        )

    elif data.installation_cost_lkr is None:
        missing_inputs.append(
            "installation_cost_lkr"
        )

    calculation_ready = (
        annual_consumption is not None
        and generation is not None
    )

    financial_ready = (
        annual_benefit is not None
        and data.installation_cost_lkr is not None
    )

    assumptions.append(
        "This is a planning estimate and not a "
        "professional engineering design."
    )

    return SolarPlanningScenario(
        system_capacity_kw=
            data.system_capacity_kw,

        annual_consumption_kwh=
            annual_consumption,

        estimated_annual_generation_kwh=
            generation,

        self_consumed_solar_kwh=
            self_consumed,

        exported_solar_kwh=
            exported,

        grid_import_kwh=
            grid_import,

        energy_coverage_percent=
            coverage,

        avoided_import_cost_lkr=
            avoided_cost,

        export_income_lkr=
            export_income,

        estimated_annual_benefit_lkr=
            annual_benefit,

        simple_payback_years=
            payback,

        calculation_ready=
            calculation_ready,

        financial_calculation_ready=
            financial_ready,

        missing_inputs=
            sorted(set(missing_inputs)),

        assumptions=
            assumptions,
    )