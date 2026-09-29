import httpx

from app.core.config import settings


def create_embedding(
    text: str,
) -> list[float]:

    response = httpx.post(
        f"{settings.ollama_base_url}/api/embeddings",
        json={
            "model":
                settings.embedding_model,

            "prompt":
                text,
        },
        timeout=settings.llm_timeout_seconds,
    )

    response.raise_for_status()

    data = response.json()

    return data["embedding"]