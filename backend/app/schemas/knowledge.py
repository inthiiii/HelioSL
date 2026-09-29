from pydantic import BaseModel, Field


class KnowledgeSearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=2000,
    )
    top_k: int | None = Field(
        default=None,
        ge=1,
        le=20,
    )


class RetrievedSource(BaseModel):
    title: str
    organization: str | None
    source_url: str | None
    chunk: str


class KnowledgeSearchResponse(BaseModel):
    query: str
    results: list[RetrievedSource]
