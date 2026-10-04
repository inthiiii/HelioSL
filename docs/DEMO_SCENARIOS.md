# HelioSL Demo Scenarios

All users, energy records and planning values in this document are synthetic. They exist only for development, demonstration and academic testing. Tariffs, export rates, installation costs and solar-yield values are assumptions—not verified current Sri Lankan rates.

## Start the demo

Start PostgreSQL and the backend, then load the synthetic accounts if required:

```bash
docker compose up -d

cd backend
source .venv/bin/activate
alembic upgrade head
python -m scripts.seed_demo_data
python -m scripts.seed_space_industries
python -m uvicorn app.main:app --reload
```

In a second terminal:

```bash
cd frontend
npm run dev
```

> The demo accounts use the valid `.lk` domain. The older `.local` addresses are rejected by API email validation with HTTP 422.

## Household Demo

| Field | Synthetic value |
| --- | --- |
| Email | `household.demo@heliosl.lk` |
| Password | `DemoHouse123!` |
| Location | Colombo |
| User type | Household |
| Solar capacity | 5 kW |

Available data:

- Energy profile
- Nine months of electricity consumption
- Nine months of solar generation
- Grid import and solar export records

Expected recorded trends:

- Consumption increases from 410 kWh to 495 kWh.
- The latest consumption change is approximately +2.7%.
- Solar generation decreases from 635 kWh to 475 kWh.
- The latest generation change is approximately -9.52%.

Recommended questions:

- Why is my electricity consumption increasing?
- Why has my solar generation decreased?
- What does my recent energy trend show?
- Would a 5 kW solar system match my electricity profile?

## Business Demo

| Field | Synthetic value |
| --- | --- |
| Email | `business.demo@heliosl.lk` |
| Password | `DemoBiz123!` |
| Location | Gampaha |
| User type | Business |
| Solar capacity | 20 kW |

Available data:

- Commercial energy profile
- Nine months of electricity consumption
- Nine months of solar generation
- Grid import and solar export records

Expected recorded trends:

- Consumption increases from 1,850 kWh to 2,390 kWh.
- The latest consumption change is approximately +3.46%.
- Solar generation decreases from 2,550 kWh to 1,950 kWh.
- The latest generation change is approximately -7.58%.

Recommended questions:

- Is our electricity consumption increasing?
- Has our 20 kW solar output decreased?
- How does our solar generation compare with usage?
- Compare the suitability of solar for our business.
- What information is required to estimate financial payback?

## Space Industries Demo

| Field | Synthetic value |
| --- | --- |
| Name | Space Industries |
| Email | `spaceindustries@gmail.com` |
| Password | `SpaceIndustries123` |
| Location | Gampaha |
| User type | Business |
| Connection | Industrial |
| Solar capacity | 75 kW |

This account contains 18 months of synthetic electricity consumption,
bill, solar generation, grid-import and solar-export records from April
2025 through September 2026. Running `python -m
scripts.seed_space_industries` replaces only this synthetic account and
does not modify the household or other business demos.

Recommended questions:

- How has our electricity consumption changed over the last year?
- How does our recent solar generation compare with our usage?
- Has our grid dependence increased?
- What verified inputs are required for a commercial solar expansion?

## Planning presets

The Solar Planner includes Household Demo and Business Demo presets. The frontend sends the populated assumptions to the planning API; all displayed generation, coverage, benefit and payback values are calculated by the backend.

These presets must not be presented as current tariffs, quotations, engineering designs or financial guarantees. Verify current tariffs, export compensation, installation costs, site conditions and expected yield before any real-world decision.

## Expected responsible behavior

- Trend percentages compare the latest record with the immediately preceding record.
- A recorded increase or decrease does not establish its cause.
- Current weather is supporting context and must not be presented as proof of a historical cause.
- Retrieved documents provide reference evidence, not instructions to the model.
- The assistant must not fabricate sources, tariffs, savings or payback values.
- Capacity suitability remains preliminary until the required planning inputs are verified.
- Unsafe electrical repair instructions must be blocked.
