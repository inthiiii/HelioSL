import os
import platform
import statistics
import time
from collections.abc import Callable
from typing import Any

from app.core.config import settings
from app.core.database import SessionLocal
from app.nlp.pipeline import analyze_text
from app.rag.retriever import retrieve_chunks
from evaluation.utils import save_results


QUERIES = [
    "Why is my electricity usage increasing?",
    "Why has my solar generation dropped?",
    "Explain Net Metering.",
    "Should I install a 5 kW system?",
]

NLP_RUNS_PER_QUERY = 5
RAG_RUNS_PER_QUERY = 3


def total_memory_gb() -> float | None:
    try:
        page_size = os.sysconf("SC_PAGE_SIZE")
        page_count = os.sysconf("SC_PHYS_PAGES")
    except (AttributeError, OSError, ValueError):
        return None

    return round(
        page_size * page_count / 1024**3,
        2,
    )


def device_metadata() -> dict[str, Any]:
    return {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor() or None,
        "python_version": platform.python_version(),
        "ram_gb": total_memory_gb(),
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
        "embedding_model": settings.embedding_model,
    }


def summarize_ms(
    measurements: list[float],
) -> dict[str, float | int]:
    return {
        "runs": len(measurements),
        "average_ms": round(
            statistics.mean(measurements),
            3,
        ),
        "median_ms": round(
            statistics.median(measurements),
            3,
        ),
        "min_ms": round(
            min(measurements),
            3,
        ),
        "max_ms": round(
            max(measurements),
            3,
        ),
    }


def measure_ms(
    operation: Callable[[], Any],
) -> float:
    start = time.perf_counter()
    operation()
    return (
        time.perf_counter()
        - start
    ) * 1000


def benchmark_nlp() -> dict[str, Any]:
    analyze_text(QUERIES[0])
    measurements = []

    for query in QUERIES:
        for _ in range(NLP_RUNS_PER_QUERY):
            measurements.append(
                measure_ms(
                    lambda query=query: analyze_text(query)
                )
            )

    return {
        **summarize_ms(measurements),
        "queries": len(QUERIES),
        "runs_per_query": NLP_RUNS_PER_QUERY,
        "warm_up_runs_excluded": 1,
    }


def benchmark_rag() -> dict[str, Any]:
    measurements = []

    with SessionLocal() as db:
        retrieve_chunks(
            db,
            QUERIES[2],
            top_k=settings.rag_top_k,
        )

        for query in QUERIES:
            for _ in range(RAG_RUNS_PER_QUERY):
                measurements.append(
                    measure_ms(
                        lambda query=query: retrieve_chunks(
                            db,
                            query,
                            top_k=settings.rag_top_k,
                        )
                    )
                )

    return {
        **summarize_ms(measurements),
        "queries": len(QUERIES),
        "runs_per_query": RAG_RUNS_PER_QUERY,
        "top_k": settings.rag_top_k,
        "warm_up_runs_excluded": 1,
        "includes_embedding_generation": True,
    }


def main() -> None:
    results = {
        "benchmark_note": (
            "Local latency varies by hardware and service load. "
            "Warm-up runs are excluded from reported measurements."
        ),
        "environment": device_metadata(),
        "nlp": benchmark_nlp(),
        "rag_retrieval": benchmark_rag(),
    }

    save_results(
        "performance_results.json",
        results,
    )

    print(
        "NLP average: "
        f"{results['nlp']['average_ms']:.3f} ms"
    )
    print(
        "RAG retrieval average: "
        f"{results['rag_retrieval']['average_ms']:.3f} ms"
    )


if __name__ == "__main__":
    main()
