from sqlalchemy.orm import Session

from app.llm.client import get_llm_client
from app.rag.retriever import retrieve_chunks


RAG_SYSTEM_PROMPT = """
You are HelioSL, a Sri Lankan renewable-energy assistant.

Answer using ONLY the supplied retrieved context
for factual renewable-energy claims.

If the context does not contain enough information,
state that clearly.

Do not invent regulations, tariffs, schemes,
organizations, or sources.

When appropriate, explain uncertainty clearly.
"""


def generate_rag_answer(
    db: Session,
    query: str,
):
    chunks = retrieve_chunks(
        db,
        query,
    )

    if not chunks:
        return {
            "answer": (
                "I could not find enough trusted "
                "information in the HelioSL "
                "knowledge base."
            ),
            "sources": [],
        }

    context_parts = []

    sources = []

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

{chunk.content}
"""
        )

        sources.append(
            {
                "number": index,
                "title": document.title,
                "organization":
                    document.organization,
                "source_url":
                    document.source_url,
            }
        )

    context = "\n".join(
        context_parts
    )

    prompt = f"""
Retrieved context:

{context}

User question:

{query}

Answer the question using the retrieved context.
"""

    client = get_llm_client()

    answer = client.generate(
        prompt=prompt,
        system_prompt=RAG_SYSTEM_PROMPT,
    )

    return {
        "answer": answer,
        "sources": sources,
    }