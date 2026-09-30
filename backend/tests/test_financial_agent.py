from app.agents.financial_agent import (
    run_financial_agent,
)


def test_financial_agent_consumption_conversion():

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

    assert (
        financial[
            "estimated_daily_consumption_kwh"
        ]
        == 15.0
    )

    assert (
        financial[
            "requested_capacity_kw"
        ]
        == 5.0
    )