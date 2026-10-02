from app.core.database import SessionLocal
from app.rag.retriever import retrieve_chunks

from evaluation.utils import load_dataset, save_results


TOP_K = 5


def main() -> None:
    db = SessionLocal()

    try:
        cases = load_dataset(
            "retrieval_cases.json"
        )

        results = []
        successful = 0

        for case in cases:
            chunks = retrieve_chunks(
                db,
                case["query"],
                top_k=TOP_K,
            )

            expected_keywords = [
                word.lower()
                for word in case.get(
                    "expected_keywords",
                    [],
                )
            ]

            organizations = [
                value.lower()
                for value in case.get(
                    "expected_organizations",
                    [],
                )
            ]

            combined_content = " ".join(
                chunk.content.lower()
                for chunk in chunks
            )

            retrieved_orgs = {
                (
                    chunk.document.organization
                    or ""
                ).lower()
                for chunk in chunks
            }

            keyword_match = (
                any(
                    keyword in combined_content
                    for keyword in expected_keywords
                )
                if expected_keywords
                else True
            )

            organization_match = (
                any(
                    org in retrieved_orgs
                    for org in organizations
                )
                if organizations
                else True
            )

            passed = (
                keyword_match
                and organization_match
            )

            if passed:
                successful += 1

            results.append(
                {
                    "query": case["query"],
                    "result_count": len(chunks),
                    "keyword_match": keyword_match,
                    "organization_match": organization_match,
                    "passed": passed,
                    "retrieved_titles": [
                        chunk.document.title
                        for chunk in chunks
                    ],
                }
            )

        recall_proxy = (
            successful
            / len(cases)
            * 100
            if cases
            else 0
        )

        output = {
            "metric_note": (
                "Keyword and organization matching is a retrieval "
                "success proxy, not human-judged relevance."
            ),
            "top_k": TOP_K,
            "total_cases": len(cases),
            "successful_cases": successful,
            "retrieval_success_percent": round(
                recall_proxy,
                2,
            ),
            "cases": results,
        }

        save_results(
            "retrieval_results.json",
            output,
        )

        print(
            "Retrieval success: "
            f"{recall_proxy:.2f}%"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()
