from app.agents.orchestrator import (
    orchestrator_agent,
)
from app.nlp.pipeline import analyze_text

from evaluation.utils import (
    load_dataset,
    save_results,
)


def main():
    cases = load_dataset(
        "routing_cases.json"
    )

    correct = 0
    results = []

    for case in cases:
        analysis = analyze_text(
            case["query"]
        )

        state = {
            "original_query":
                case["query"],

            "normalized_query":
                analysis[
                    "normalized_query"
                ],

            "intent":
                analysis["intent"],

            "entities":
                analysis["entities"],

            "trace": [],
        }

        result = orchestrator_agent(
            state
        )

        expected = set(
            case["expected_agents"]
        )

        actual = set(
            result.get(
                "selected_agents",
                [],
            )
        )

        matched = expected == actual

        if matched:
            correct += 1

        results.append(
            {
                "query":
                    case["query"],

                "expected_agents":
                    sorted(expected),

                "actual_agents":
                    sorted(actual),

                "correct":
                    matched,
            }
        )

    accuracy = (
        correct
        / len(cases)
        * 100
        if cases
        else 0
    )

    output = {
        "total_cases":
            len(cases),

        "correct":
            correct,

        "routing_accuracy_percent":
            round(
                accuracy,
                2,
            ),

        "cases":
            results,
    }

    save_results(
        "routing_results.json",
        output,
    )

    print(
        f"Routing accuracy: "
        f"{accuracy:.2f}%"
    )


if __name__ == "__main__":
    main()