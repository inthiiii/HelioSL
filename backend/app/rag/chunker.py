from app.core.config import settings


def chunk_text(
    text: str,
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[str]:

    chunk_size = (
        chunk_size
        or settings.rag_chunk_size
    )

    overlap = (
        overlap
        or settings.rag_chunk_overlap
    )

    cleaned = " ".join(
        text.split()
    )

    chunks: list[str] = []

    start = 0

    while start < len(cleaned):
        end = start + chunk_size

        chunk = cleaned[
            start:end
        ].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(cleaned):
            break

        start = end - overlap

    return chunks