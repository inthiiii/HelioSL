from typing import Any

from pydantic import BaseModel, Field


class AssistantRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
    )


class AssistantResponse(BaseModel):
    message: str
    intent: str
    entities: dict[str, Any]
    normalized_query: str
    provider: str
    model: str
    disclaimer: str