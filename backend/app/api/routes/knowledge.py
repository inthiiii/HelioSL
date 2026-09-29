from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.rag.retriever import retrieve_chunks
from app.schemas.knowledge import (
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
    RetrievedSource,
)
from app.security.dependencies import get_current_user


router = APIRouter()


@router.post(
    "/search",
    response_model=KnowledgeSearchResponse,
)
def search_knowledge(
    data: KnowledgeSearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> KnowledgeSearchResponse:
    chunks = retrieve_chunks(
        db=db,
        query=data.query,
        top_k=data.top_k,
    )

    return KnowledgeSearchResponse(
        query=data.query,
        results=[
            RetrievedSource(
                title=chunk.document.title,
                organization=chunk.document.organization,
                source_url=chunk.document.source_url,
                chunk=chunk.content,
            )
            for chunk in chunks
        ],
    )
