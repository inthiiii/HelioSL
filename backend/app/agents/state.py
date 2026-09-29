from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    user_id: int

    original_query: str
    normalized_query: str

    intent: str
    entities: dict[str, Any]

    selected_agents: list[str]

    energy_result: dict[str, Any]
    knowledge_result: dict[str, Any]
    financial_result: dict[str, Any]

    combined_context: str

    draft_answer: str

    safety_passed: bool
    safety_notes: list[str]

    final_answer: str
    sources: list[dict[str, Any]]

    trace: list[str]