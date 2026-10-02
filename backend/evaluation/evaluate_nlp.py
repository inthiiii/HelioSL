from app.nlp.pipeline import analyze_text

from evaluation.utils import (
    load_dataset,
    save_results,
)


def main():
    cases = load_dataset(
        "nlp_cases.json"
    )

    results = []

    intent_correct = 0

    entity_checks = 0
    entity_correct = 0

    for case in cases:
        analysis = analyze_text(
            case["query"]
        )

        intent_match = (
            analysis["intent"]
            == case["expected_intent"]
        )

        if intent_match:
            intent_correct += 1

        expected_entities = case.get(
            "expected_entities",
            {},
        )

        entity_results = {}

        for key, expected in (
            expected_entities.items()
        ):
            actual = analysis[
                "entities"
            ].get(key)

            matched = actual == expected

            entity_results[key] = {
                "expected": expected,
                "actual": actual,
                "correct": matched,
            }

            entity_checks += 1

            if matched:
                entity_correct += 1

        results.append(
            {
                "query": case["query"],
                "expected_intent":
                    case["expected_intent"],
                "actual_intent":
                    analysis["intent"],
                "intent_correct":
                    intent_match,
                "entities":
                    entity_results,
            }
        )

    intent_accuracy = (
        intent_correct
        / len(cases)
        * 100
        if cases
        else 0
    )

    entity_accuracy = (
        entity_correct
        / entity_checks
        * 100
        if entity_checks
        else None
    )

    summary = {
        "total_cases":
            len(cases),

        "intent_correct":
            intent_correct,

        "intent_accuracy_percent":
            round(
                intent_accuracy,
                2,
            ),

        "entity_checks":
            entity_checks,

        "entity_accuracy_percent":
            (
                round(
                    entity_accuracy,
                    2,
                )
                if entity_accuracy
                is not None
                else None
            ),

        "cases":
            results,
    }

    save_results(
        "nlp_results.json",
        summary,
    )

    print(
        f"Intent accuracy: "
        f"{intent_accuracy:.2f}%"
    )

    if entity_accuracy is not None:
        print(
            f"Entity accuracy: "
            f"{entity_accuracy:.2f}%"
        )


if __name__ == "__main__":
    main()