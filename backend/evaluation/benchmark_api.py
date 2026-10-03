import os
import platform
import statistics
import time
from typing import Any

import httpx

from app.core.config import settings
from evaluation.utils import save_results


BASE_URL = os.getenv(
    "HELIOSL_API_BASE_URL",
    "http://127.0.0.1:8000/api/v1",
).rstrip("/")

DEMO_EMAIL = os.getenv(
    "HELIOSL_BENCHMARK_EMAIL",
    "household.demo@heliosl.lk",
)
DEMO_PASSWORD = os.getenv(
    "HELIOSL_BENCHMARK_PASSWORD",
    "DemoHouse123!",
)

ASSISTANT_QUESTIONS = [
    "Why is my electricity usage increasing?",
    "Why has my solar generation dropped?",
    "Explain Net Metering in Sri Lanka.",
    "Should I install a 5 kW solar system?",
    "Explain my recent energy trend.",
]

PLANNING_PAYLOAD = {
    "system_capacity_kw": 5,
    "installation_cost_lkr": 1_250_000,
    "import_tariff_lkr_per_kwh": 50,
    "export_rate_lkr_per_kwh": 27,
    "specific_yield_kwh_per_kw_year": 1400,
    "self_consumption_ratio": 0.40,
}

PLANNING_RUNS = 5


def summarize_seconds(
    measurements: list[float],
) -> dict[str, float | int]:
    return {
        "runs": len(measurements),
        "average_seconds": round(
            statistics.mean(measurements),
            3,
        ),
        "median_seconds": round(
            statistics.median(measurements),
            3,
        ),
        "min_seconds": round(
            min(measurements),
            3,
        ),
        "max_seconds": round(
            max(measurements),
            3,
        ),
    }


def timed_post(
    client: httpx.Client,
    path: str,
    headers: dict[str, str],
    payload: dict[str, Any],
) -> tuple[httpx.Response, float]:
    start = time.perf_counter()
    response = client.post(
        f"{BASE_URL}{path}",
        headers=headers,
        json=payload,
    )
    elapsed = time.perf_counter() - start
    response.raise_for_status()
    return response, elapsed


def benchmark_agentic(
    client: httpx.Client,
    headers: dict[str, str],
) -> dict[str, Any]:
    measurements = []
    runs = []

    for question in ASSISTANT_QUESTIONS:
        response, elapsed = timed_post(
            client,
            "/assistant/agentic",
            headers,
            {"message": question},
        )
        data = response.json()
        measurements.append(elapsed)
        runs.append(
            {
                "query": question,
                "elapsed_seconds": round(elapsed, 3),
                "intent": data.get("intent"),
                "selected_agents": data.get(
                    "selected_agents",
                    [],
                ),
                "safety_passed": data.get("safety_passed"),
            }
        )
        print(
            question,
            round(elapsed, 2),
            "seconds",
        )

    return {
        **summarize_seconds(measurements),
        "requests": runs,
    }


def benchmark_planning(
    client: httpx.Client,
    headers: dict[str, str],
) -> dict[str, Any]:
    measurements = []

    for _ in range(PLANNING_RUNS):
        _, elapsed = timed_post(
            client,
            "/planning/scenario",
            headers,
            PLANNING_PAYLOAD,
        )
        measurements.append(elapsed)

    return summarize_seconds(measurements)


def main() -> None:
    with httpx.Client(timeout=120) as client:
        login_start = time.perf_counter()
        login = client.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": DEMO_EMAIL,
                "password": DEMO_PASSWORD,
            },
        )
        login_elapsed = time.perf_counter() - login_start
        login.raise_for_status()

        token = login.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}"
        }

        results = {
            "benchmark_note": (
                "End-to-end HTTP latency measured against a local "
                "development server. Login is reported separately."
            ),
            "environment": {
                "platform": platform.platform(),
                "machine": platform.machine(),
                "python_version": platform.python_version(),
                "llm_provider": settings.llm_provider,
                "llm_model": settings.llm_model,
                "embedding_model": settings.embedding_model,
                "base_url": BASE_URL,
                "test_user": DEMO_EMAIL,
            },
            "login_seconds": round(login_elapsed, 3),
            "agentic_api": benchmark_agentic(
                client,
                headers,
            ),
            "planning_api": benchmark_planning(
                client,
                headers,
            ),
        }

    save_results(
        "api_performance_results.json",
        results,
    )

    print(
        "Agentic API average: "
        f"{results['agentic_api']['average_seconds']:.3f} seconds"
    )
    print(
        "Planning API average: "
        f"{results['planning_api']['average_seconds']:.3f} seconds"
    )


if __name__ == "__main__":
    main()
