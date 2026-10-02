from app.agents.financial_agent import (
    run_financial_agent,
)


def test_financial_agent_uses_available_planning_inputs():

    state = {
        "energy_result": {
            "average_consumption_kwh": 450,
            "latest_consumption_kwh": 470,
            "average_generation_kwh": 520,
        },
        "entities": {
            "capacity_kw": 5.0,
        },
        "trace": [],
    }

    result = run_financial_agent(
        state
    )

    financial = result[
        "financial_result"
    ]

    assert financial["monthly_consumption_kwh"] == 450

    assert (
        financial[
            "requested_capacity_kw"
        ]
        == 5.0
    )

    assert financial["financial_calculation_ready"] is False
    assert financial["missing_inputs"] == []


def test_financial_agent_identifies_missing_core_inputs():
    result = run_financial_agent(
        {
            "energy_result": {},
            "entities": {},
            "trace": [],
        }
    )

    financial = result["financial_result"]

    assert financial["monthly_consumption_kwh"] is None
    assert financial["requested_capacity_kw"] is None
    assert financial["missing_inputs"] == [
        "monthly_consumption",
        "system_capacity_kw",
    ]


def test_financial_agent_uses_recorded_system_capacity():
    result = run_financial_agent(
        {
            "energy_result": {
                "average_consumption_kwh": 2114.44,
                "solar_capacity_kw": 20.0,
            },
            "entities": {},
            "trace": [],
        }
    )

    financial = result["financial_result"]

    assert financial["monthly_consumption_kwh"] == 2114.44
    assert financial["requested_capacity_kw"] == 20.0
    assert financial["missing_inputs"] == []
