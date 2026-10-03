import json
from pathlib import Path
from typing import Any


RESULTS_DIR = (
    Path(__file__).resolve().parent
    / "results"
)


def read_json(
    name: str,
) -> dict[str, Any] | None:
    path = RESULTS_DIR / name

    if not path.exists():
        return None

    return json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )


def percent(value: Any) -> str:
    if value is None:
        return "Unavailable"

    return f"{float(value):.2f}%"


def number(value: Any, unit: str = "") -> str:
    if value is None:
        return "Unavailable"

    return f"{value}{unit}"


def add_unavailable(
    lines: list[str],
    filename: str,
) -> None:
    lines.extend(
        [
            (
                f"No results were available. Run the evaluator that "
                f"creates `{filename}` and regenerate this report."
            ),
            "",
        ]
    )


def main() -> None:
    nlp = read_json("nlp_results.json")
    routing = read_json("routing_results.json")
    retrieval = read_json("retrieval_results.json")
    answer_quality = read_json("answer_quality_results.json")
    performance = read_json("performance_results.json")
    api_performance = read_json("api_performance_results.json")
    demo = read_json("demo_scenario_results.json")

    lines = [
        "# HelioSL System Evaluation",
        "",
        (
            "This report consolidates the automated and human-scored "
            "evaluation artifacts produced for HelioSL."
        ),
        "",
        "## Executive Summary",
        "",
        "| Evaluation | Result |",
        "| --- | ---: |",
        (
            "| NLP intent accuracy | "
            f"{percent(nlp.get('intent_accuracy_percent') if nlp else None)} |"
        ),
        (
            "| Entity extraction accuracy | "
            f"{percent(nlp.get('entity_accuracy_percent') if nlp else None)} |"
        ),
        (
            "| Agent routing accuracy | "
            f"{percent(routing.get('routing_accuracy_percent') if routing else None)} |"
        ),
        (
            "| Retrieval success proxy | "
            f"{percent(retrieval.get('retrieval_success_percent') if retrieval else None)} |"
        ),
        (
            "| Human answer-quality score | "
            f"{percent(answer_quality.get('summary', {}).get('score_percent_for_completed_cases') if answer_quality else None)} |"
        ),
        (
            "| End-to-end scenario pass rate | "
            f"{percent(demo.get('scenario_matrix', {}).get('pass_rate_percent') if demo else None)} |"
        ),
        (
            "| Project security-suite pass rate | "
            f"{percent(demo.get('security_test_pass_rate', {}).get('pass_rate_percent') if demo else None)} |"
        ),
        "",
        "## NLP Evaluation",
        "",
    ]

    if nlp:
        lines.extend(
            [
                f"- Cases: {nlp.get('total_cases', 0)}",
                f"- Intent accuracy: {percent(nlp.get('intent_accuracy_percent'))}",
                (
                    "- Entity extraction accuracy: "
                    f"{percent(nlp.get('entity_accuracy_percent'))}"
                ),
                "",
            ]
        )

        incorrect = [
            case
            for case in nlp.get("cases", [])
            if not case.get("intent_correct", False)
        ]
        if incorrect:
            lines.extend(
                [
                    "### Intent errors",
                    "",
                ]
            )
            for case in incorrect:
                lines.append(
                    f"- `{case.get('query', '')}`: expected "
                    f"`{case.get('expected_intent')}`, received "
                    f"`{case.get('actual_intent')}`."
                )
            lines.append("")
    else:
        add_unavailable(lines, "nlp_results.json")

    lines.extend(
        [
            "## Agent Routing",
            "",
        ]
    )

    if routing:
        lines.extend(
            [
                f"- Cases: {routing.get('total_cases', 0)}",
                (
                    "- Correct routes: "
                    f"{routing.get('correct', 0)}"
                ),
                (
                    "- Routing accuracy: "
                    f"{percent(routing.get('routing_accuracy_percent'))}"
                ),
                "",
            ]
        )

        failed_routes = [
            case
            for case in routing.get("cases", [])
            if not case.get("correct", False)
        ]
        if failed_routes:
            lines.extend(["### Routing errors", ""])
            for case in failed_routes:
                lines.append(
                    f"- `{case.get('query', '')}`: expected "
                    f"`{case.get('expected_agents', [])}`, received "
                    f"`{case.get('actual_agents', [])}`."
                )
            lines.append("")
    else:
        add_unavailable(lines, "routing_results.json")

    lines.extend(
        [
            "## Retrieval",
            "",
        ]
    )

    if retrieval:
        lines.extend(
            [
                f"- Queries: {retrieval.get('total_cases', 0)}",
                f"- Top K: {retrieval.get('top_k', 'Unavailable')}",
                (
                    "- Retrieval benchmark success: "
                    f"{percent(retrieval.get('retrieval_success_percent'))}"
                ),
                (
                    "- Interpretation: this is a keyword-and-organization "
                    "matching proxy, not human-judged relevance or Precision@K."
                ),
                "",
            ]
        )
    else:
        add_unavailable(lines, "retrieval_results.json")

    lines.extend(
        [
            "## Human Answer-Quality Evaluation",
            "",
        ]
    )

    if answer_quality:
        summary = answer_quality.get("summary", {})
        lines.extend(
            [
                f"- Completed cases: {summary.get('completed_cases', 0)}",
                (
                    "- Average score: "
                    f"{number(summary.get('average_total_score'))}/10"
                ),
                (
                    "- Overall score: "
                    f"{percent(summary.get('score_percent_for_completed_cases'))}"
                ),
                "",
                "| Metric | Average (0–2) |",
                "| --- | ---: |",
            ]
        )
        averages = summary.get("average_score_by_metric", {})
        for metric in (
            "correctness",
            "groundedness",
            "safety",
            "transparency",
            "relevance",
        ):
            lines.append(
                f"| {metric.replace('_', ' ').title()} | "
                f"{number(averages.get(metric))} |"
            )
        lines.append("")

        weakest = sorted(
            answer_quality.get("cases", []),
            key=lambda case: case.get("total_score", 0),
        )[:3]
        if weakest:
            lines.extend(["### Lowest-scoring responses", ""])
            for case in weakest:
                lines.append(
                    f"- **{case.get('id', 'Unknown')} — "
                    f"{case.get('total_score', 0)}/10:** "
                    f"{case.get('notes', 'No notes recorded.')}"
                )
            lines.append("")
    else:
        add_unavailable(lines, "answer_quality_results.json")

    lines.extend(
        [
            "## Performance",
            "",
        ]
    )

    if performance:
        environment = performance.get("environment", {})
        nlp_perf = performance.get("nlp", {})
        rag_perf = performance.get("rag_retrieval", {})
        lines.extend(
            [
                f"- Test platform: {environment.get('platform', 'Unavailable')}",
                f"- RAM: {number(environment.get('ram_gb'), ' GB')}",
                f"- LLM: {environment.get('llm_provider', 'Unavailable')} / "
                f"{environment.get('llm_model', 'Unavailable')}",
                f"- NLP average: {number(nlp_perf.get('average_ms'), ' ms')}",
                (
                    "- RAG retrieval average: "
                    f"{number(rag_perf.get('average_ms'), ' ms')}"
                ),
                "",
            ]
        )
    else:
        add_unavailable(lines, "performance_results.json")

    if api_performance:
        agentic = api_performance.get("agentic_api", {})
        planning = api_performance.get("planning_api", {})
        lines.extend(
            [
                "### API latency",
                "",
                (
                    "- Agentic assistant average: "
                    f"{number(agentic.get('average_seconds'), ' seconds')} "
                    f"across {agentic.get('runs', 0)} runs"
                ),
                (
                    "- Planning API average: "
                    f"{number(planning.get('average_seconds'), ' seconds')} "
                    f"across {planning.get('runs', 0)} runs"
                ),
                "",
            ]
        )

    lines.extend(
        [
            "## Household, Business and Security Evaluation",
            "",
        ]
    )

    if demo:
        household = demo.get("personas", {}).get("household", {})
        business = demo.get("personas", {}).get("business", {})
        matrix = demo.get("scenario_matrix", {})
        security = demo.get("security_test_pass_rate", {})
        lines.extend(
            [
                "| Persona | Average monthly consumption | Solar capacity | Records |",
                "| --- | ---: | ---: | ---: |",
                (
                    "| Household | "
                    f"{number(household.get('average_monthly_consumption_kwh'), ' kWh')} | "
                    f"{number(household.get('solar_capacity_kw'), ' kW')} | "
                    f"{household.get('consumption_record_count', 0)} consumption / "
                    f"{household.get('generation_record_count', 0)} generation |"
                ),
                (
                    "| Business | "
                    f"{number(business.get('average_monthly_consumption_kwh'), ' kWh')} | "
                    f"{number(business.get('solar_capacity_kw'), ' kW')} | "
                    f"{business.get('consumption_record_count', 0)} consumption / "
                    f"{business.get('generation_record_count', 0)} generation |"
                ),
                "",
                (
                    "- Cross-user data isolation: "
                    f"{'Passed' if demo.get('data_isolation', {}).get('passed') else 'Failed'}"
                ),
                (
                    "- Persona planning comparison: "
                    f"{'Passed' if demo.get('planning_comparison', {}).get('passed') else 'Failed'}"
                ),
                (
                    "- End-to-end scenario matrix: "
                    f"{matrix.get('passed_scenarios', 0)}/{matrix.get('total_scenarios', 0)} "
                    f"passed ({percent(matrix.get('pass_rate_percent'))})"
                ),
                (
                    "- Project security suite: "
                    f"{security.get('passed', 0)}/{security.get('total', 0)} "
                    f"passed ({percent(security.get('pass_rate_percent'))})"
                ),
                "",
            ]
        )
    else:
        add_unavailable(lines, "demo_scenario_results.json")

    lines.extend(
        [
            "## Interpretation and Limitations",
            "",
            (
                "- The strongest measured areas are entity extraction, the "
                "retrieval proxy, scenario execution, data isolation and the "
                "project security suite."
            ),
            (
                "- Intent classification and routing require further work, "
                "particularly for financial and scheme-selection questions."
            ),
            (
                "- The human evaluation identified important answer-quality "
                "issues, including unsafe inverter guidance and an incorrect "
                "RTSPV definition. These scores must not be replaced with an "
                "LLM judging its own output."
            ),
            (
                "- Retrieval success is a proxy. A separately labelled human "
                "Precision@5 evaluation is required before claiming retrieval "
                "accuracy."
            ),
            (
                "- Latency values describe the recorded local test device and "
                "model; they are not production service-level guarantees."
            ),
            "",
            "## Result Artifacts",
            "",
        ]
    )

    for filename in (
        "nlp_results.json",
        "routing_results.json",
        "retrieval_results.json",
        "answer_quality_results.json",
        "performance_results.json",
        "api_performance_results.json",
        "demo_scenario_results.json",
    ):
        if (RESULTS_DIR / filename).exists():
            lines.append(f"- `{filename}`")

    lines.append("")

    output = RESULTS_DIR / "EVALUATION_REPORT.md"
    output.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Created: {output}")


if __name__ == "__main__":
    main()
