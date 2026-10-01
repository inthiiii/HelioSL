from sqlalchemy import case, func, select
from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.models.knowledge import (
    KnowledgeChunk,
    KnowledgeDocument,
)
from app.rag.embeddings import (
    create_embedding,
)


def normalize_retrieval_query(query: str) -> str:
    normalized = " ".join(query.split())
    lowered = normalized.lower()

    if "inverter" in lowered:
        return (
            f"{normalized} rooftop solar PV installation guideline "
            "technical inverter protection and safety requirements"
        )

    if "bess" in lowered or "battery storage" in lowered:
        return (
            f"{normalized} RTSPV BESS interconnection operation "
            "distribution licensee prosumer guideline"
        )

    return normalized


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
        normalize_retrieval_query(query)
    )

    semantic_distance = (
        KnowledgeChunk.embedding.cosine_distance(
            query_embedding
        )
    )

    authority_penalty = case(
        (KnowledgeDocument.authority_level == 1, 0.0),
        (KnowledgeDocument.authority_level == 2, 0.025),
        (KnowledgeDocument.authority_level == 3, 0.05),
        else_=0.075,
    )

    source_year = func.coalesce(
        func.extract(
            "year",
            KnowledgeDocument.effective_date,
        ),
        KnowledgeDocument.published_year,
        func.extract("year", func.current_date()),
    )

    recency_penalty = func.least(
        func.greatest(
            (
                func.extract("year", func.current_date())
                - source_year
            )
            * 0.002,
            0.0,
        ),
        0.04,
    )

    ranking_score = (
        semantic_distance
        + authority_penalty
        + recency_penalty
    )

    statement = (
        select(KnowledgeChunk)
        .join(KnowledgeChunk.document)
        .options(
            joinedload(KnowledgeChunk.document)
        )
        .where(
            KnowledgeChunk.embedding.is_not(None)
        )
        .order_by(
            ranking_score
        )
        .limit(top_k)
    )

    return list(
        db.scalars(statement).all()
    )
