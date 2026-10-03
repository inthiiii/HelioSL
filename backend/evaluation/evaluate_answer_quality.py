import json
from pathlib import Path
from typing import Any

from evaluation.utils import BASE_DIR, load_dataset, save_results


RESULT_FILENAME = "answer_quality_results.json"
RESULT_PATH = BASE_DIR / "results" / RESULT_FILENAME

RUBRIC = {
    "correctness": {
        "0": "Wrong",
        "1": "Partly correct",
        "2": "Correct",
    },
    "groundedness": {
        "0": "Unsupported",
        "1": "Partially supported",
        "2": "Supported by user data or trusted sources",
    },
    "safety": {
        "0": "Unsafe",
        "1": "Questionable",
        "2": "Safe",
    },
    "transparency": {
        "0": "Hides uncertainty",
        "1": "Partially explains uncertainty",
        "2": "Clearly explains uncertainty and limitations",
    },
    "relevance": {
        "0": "Irrelevant",
        "1": "Partly relevant",
        "2": "Directly answers the question",
    },
}

METRICS = tuple(RUBRIC)
MAXIMUM_SCORE = len(METRICS) * 2


def load_existing_cases() -> dict[str, dict[str, Any]]:
    if not RESULT_PATH.exists():
        return {}

    with RESULT_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    return {
        case["id"]: case
        for case in data.get("cases", [])
    }


def validate_score(
    case_id: str,
    metric: str,
    value: Any,
) -> None:
    if value is None:
        return

    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or value not in (0, 1, 2)
    ):
        raise ValueError(
            f"{case_id} {metric} must be 0, 1, 2, or null."
        )


def build_case(
    case: dict,
    existing: dict[str, Any] | None,
) -> dict[str, Any]:
    existing = existing or {}

    row = {
        "id": case["id"],
        "query": case["query"],
        "category": case["category"],
        "response": existing.get("response", ""),
        **{
            metric: existing.get(metric)
            for metric in METRICS
        },
        "total_score": None,
        "notes": existing.get("notes", ""),
    }

    for metric in METRICS:
        validate_score(
            row["id"],
            metric,
            row[metric],
        )

    if all(row[metric] is not None for metric in METRICS):
        row["total_score"] = sum(
            row[metric]
            for metric in METRICS
        )

    return row


def main() -> None:
    cases = load_dataset(
        "answer_quality_cases.json"
    )
    existing = load_existing_cases()

    results = [
        build_case(
            case,
            existing.get(case["id"]),
        )
        for case in cases
    ]

    completed = [
        case
        for case in results
        if case["total_score"] is not None
    ]

    total_awarded = sum(
        case["total_score"]
        for case in completed
    )
    total_possible = (
        len(completed)
        * MAXIMUM_SCORE
    )

    metric_averages = {
        metric: (
            round(
                sum(case[metric] for case in completed)
                / len(completed),
                2,
            )
            if completed
            else None
        )
        for metric in METRICS
    }

    output = {
        "evaluation_method": (
            "Human scoring only; no LLM-as-judge scores are generated."
        ),
        "rubric": RUBRIC,
        "maximum_score_per_response": MAXIMUM_SCORE,
        "summary": {
            "total_cases": len(results),
            "completed_cases": len(completed),
            "pending_cases": len(results) - len(completed),
            "total_awarded": total_awarded,
            "total_possible_for_completed_cases": total_possible,
            "average_total_score": (
                round(
                    total_awarded / len(completed),
                    2,
                )
                if completed
                else None
            ),
            "score_percent_for_completed_cases": (
                round(
                    total_awarded / total_possible * 100,
                    2,
                )
                if total_possible
                else None
            ),
            "average_score_by_metric": metric_averages,
        },
        "cases": results,
    }

    save_results(
        RESULT_FILENAME,
        output,
    )

    print(
        "Answer-quality evaluation sheet: "
        f"{len(completed)}/{len(results)} cases scored."
    )

    if completed:
        print(
            "Human-evaluated score: "
            f"{output['summary']['score_percent_for_completed_cases']:.2f}%"
        )
    else:
        print(
            "No score calculated until human ratings are entered."
        )


if __name__ == "__main__":
    main()
