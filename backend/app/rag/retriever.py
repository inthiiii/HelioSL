from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.models.knowledge import (
    KnowledgeChunk,
)
from app.rag.embeddings import (
    create_embedding,
)


def retrieve_chunks(
    db: Session,
    query: str,
    top_k: int | None = None,
) -> list[KnowledgeChunk]:

    top_k = (
        top_k
        or settings.rag_top_k
    )

    query_embedding = create_embedding(
        query
    )

    statement = (
        select(KnowledgeChunk)
        .options(
            joinedload(KnowledgeChunk.document)
        )
        .where(
            KnowledgeChunk.embedding.is_not(None)
        )
        .order_by(
            KnowledgeChunk.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(top_k)
    )

    return list(
        db.scalars(statement).all()
    )
