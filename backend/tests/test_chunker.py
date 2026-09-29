from app.rag.chunker import chunk_text


def test_chunking():
    text = "a" * 2000

    chunks = chunk_text(
        text,
        chunk_size=500,
        overlap=100,
    )

    assert len(chunks) > 1