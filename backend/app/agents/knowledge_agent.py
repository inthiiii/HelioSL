from sqlalchemy.orm import Session

from app.agents.state import AgentState
from app.rag.retriever import retrieve_chunks


def run_knowledge_agent(
    state: AgentState,
    db: Session,
) -> AgentState:

    query = state.get(
        "normalized_query"
    ) or state.get(
        "original_query",
        "",
    )

    chunks = retrieve_chunks(
        db,
        query,
    )

    context_parts: list[str] = []
    sources: list[dict] = []
    source_numbers: dict[int, int] = {}

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):
        document = chunk.document

        source_number = source_numbers.get(
            document.id
        )

        if source_number is None:
            source_number = len(sources) + 1
            source_numbers[document.id] = source_number

            sources.append(
                {
                    "number": source_number,
                    "document_id": document.id,
                    "title": document.title,
                    "organization": document.organization,
                    "published_year": document.published_year,
                    "effective_date": (
                        document.effective_date.isoformat()
                        if document.effective_date
                        else None
                    ),
                    "document_type": document.document_type,
                    "authority_level": document.authority_level,
                    "source_url": document.source_url,
                }
            )

        context_parts.append(
            f"""
SOURCE {source_number}, CHUNK {index}

Title: {document.title}
Organization: {document.organization}
Published year: {document.published_year}
Effective date: {document.effective_date or "not specified"}
Authority level: {document.authority_level}
Document type: {document.document_type}

Content:
{chunk.content}
""".strip()
        )

    result = {
        "query": query,
        "result_count": len(chunks),
        "context": "\n\n".join(
            context_parts
        ),
    }

    trace = list(
        state.get("trace", [])
    )

    if chunks:
        trace.append(
            f"Renewable Energy Knowledge Agent "
            f"retrieved {len(chunks)} trusted "
            f"knowledge chunks."
        )

    else:
        trace.append(
            "Renewable Energy Knowledge Agent "
            "found no trusted supporting documents."
        )

    return {
        **state,
        "knowledge_result": result,
        "sources": sources,
        "trace": trace,
    }
