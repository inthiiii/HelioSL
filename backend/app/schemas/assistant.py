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


class AgenticResponse(BaseModel):
    message: str
    intent: str
    entities: dict[str, Any]
    normalized_query: str
    selected_agents: list[str]
    energy_result: dict[str, Any] | None = None
    knowledge_result: dict[str, Any] | None = None
    financial_result: dict[str, Any] | None = None
    sources: list[dict[str, Any]]
    safety_passed: bool
    safety_notes: list[str]
    trace: list[str]
