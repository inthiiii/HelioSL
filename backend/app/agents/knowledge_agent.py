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

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):
        document = chunk.document

        context_parts.append(
            f"""
SOURCE {index}

Title: {document.title}
Organization: {document.organization}

Content:
{chunk.content}
""".strip()
        )

        sources.append(
            {
                "number": index,
                "document_id": document.id,
                "title": document.title,
                "organization":
                    document.organization,
                "source_url":
                    document.source_url,
            }
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