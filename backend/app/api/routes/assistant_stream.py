import json
import logging
from collections.abc import Iterator
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.agents.graph import build_agent_graph
from app.agents.state import AgentState
from app.core.database import get_db
from app.models.user import User
from app.nlp.pipeline import analyze_text
from app.schemas.assistant import (
    AgenticResponse,
    AssistantRequest,
)
from app.security.dependencies import get_current_user
from app.security.prompt_guard import (
    detect_prompt_injection,
)
from app.security.privacy import (
    redact_sensitive_data,
)
from app.security.rate_limit import limiter


logger = logging.getLogger(__name__)

router = APIRouter()


WORKFLOW_STAGES = (
    ("orchestrator", "Orchestrator"),
    ("energy", "Energy Intelligence"),
    ("weather", "Weather Intelligence"),
    ("knowledge", "Knowledge Retrieval"),
    ("financial", "Financial Planning"),
    ("generate", "Response Synthesis"),
    ("safety", "Safety Verification"),
)

OPTIONAL_AGENTS = {
    "energy",
    "weather",
    "knowledge",
    "financial",
}


def sse_event(
    event: str,
    data: dict[str, Any],
) -> str:
    return (
        f"event: {event}\n"
        f"data: {json.dumps(data)}\n\n"
    )


def _complete_label(
    agent: str,
    state: AgentState,
) -> str:
    if agent == "orchestrator":
        selected = ", ".join(
            item.title()
            for item in state.get(
                "selected_agents",
                [],
            )
        )
        return f"Selected specialist agents: {selected}"

    if agent == "energy":
        return "Historical energy data analysed"

    if agent == "weather":
        weather = state.get(
            "weather_result",
            {},
        )
        if weather.get("available"):
            return "Environmental conditions retrieved"
        return weather.get(
            "reason",
            "Weather information unavailable",
        )

    if agent == "knowledge":
        count = state.get(
            "knowledge_result",
            {},
        ).get("result_count", 0)
        if count:
            return f"Retrieved {count} trusted knowledge chunks"
        return "No trusted knowledge chunks found"

    if agent == "financial":
        return "Financial and planning context prepared"

    if agent == "generate":
        return "Specialist outputs synthesized"

    return "Safety verification complete"


def _agentic_response(
    state: AgentState,
    fallback_query: str,
) -> AgenticResponse:
    final_answer = redact_sensitive_data(
        state.get(
            "final_answer",
            "",
        )
    )

    return AgenticResponse(
        message=final_answer,
        intent=state.get("intent", "general"),
        entities=state.get("entities", {}),
        normalized_query=state.get(
            "normalized_query",
            fallback_query,
        ),
        selected_agents=state.get(
            "selected_agents",
            [],
        ),
        energy_result=state.get("energy_result"),
        weather_result=state.get("weather_result"),
        knowledge_result=state.get(
            "knowledge_result"
        ),
        financial_result=state.get(
            "financial_result"
        ),
        sources=state.get("sources", []),
        safety_passed=state.get(
            "safety_passed",
            False,
        ),
        safety_notes=state.get(
            "safety_notes",
            [],
        ),
        trace=state.get("trace", []),
    )


@router.post("/agentic/stream")
@limiter.limit("20/minute")
def stream_agentic_assistant(
    request: Request,
    data: AssistantRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    prompt_check = detect_prompt_injection(
        data.message
    )

    if prompt_check["is_suspicious"]:
        raise HTTPException(
            status_code=400,
            detail=(
                "The request contains instructions "
                "that attempt to override HelioSL's "
                "security or system behaviour."
            ),
        )

    def generate_events() -> Iterator[str]:
        active_agent = "nlp"

        try:
            yield sse_event(
                "stage",
                {
                    "agent": "nlp",
                    "status": "running",
                    "label": "Understanding your question",
                },
            )

            analysis = analyze_text(data.message)

            state: AgentState = {
                "user_id": current_user.id,
                "original_query": data.message,
                "normalized_query": analysis[
                    "normalized_query"
                ],
                "intent": analysis["intent"],
                "entities": analysis["entities"],
                "trace": [
                    "NLP normalized the query, classified "
                    "the intent and extracted entities."
                ],
            }

            yield sse_event(
                "stage",
                {
                    "agent": "nlp",
                    "status": "complete",
                    "label": "Query understood",
                },
            )

            graph_updates = iter(
                build_agent_graph(db).stream(
                    state,
                    stream_mode="updates",
                )
            )

            for agent, display_name in WORKFLOW_STAGES:
                active_agent = agent
                selected = state.get(
                    "selected_agents",
                    [],
                )
                skipped = (
                    agent in OPTIONAL_AGENTS
                    and agent not in selected
                )

                if skipped:
                    yield sse_event(
                        "stage",
                        {
                            "agent": agent,
                            "status": "skipped",
                            "label": (
                                f"{display_name} not required"
                            ),
                        },
                    )
                else:
                    yield sse_event(
                        "stage",
                        {
                            "agent": agent,
                            "status": "running",
                            "label": (
                                f"{display_name} in progress"
                            ),
                        },
                    )

                update = next(graph_updates)

                if agent not in update:
                    raise RuntimeError(
                        "Unexpected workflow update: "
                        f"expected {agent}"
                    )

                state = {
                    **state,
                    **update[agent],
                }

                if not skipped:
                    yield sse_event(
                        "stage",
                        {
                            "agent": agent,
                            "status": "complete",
                            "label": _complete_label(
                                agent,
                                state,
                            ),
                        },
                    )

            response = _agentic_response(
                state,
                data.message,
            )

            yield sse_event(
                "final",
                {
                    "answer": response.message,
                    "sources": response.sources,
                    "response": response.model_dump(
                        mode="json"
                    ),
                },
            )

        except Exception:
            logger.exception(
                "Agentic stream failed during %s",
                active_agent,
            )
            yield sse_event(
                "error",
                {
                    "agent": active_agent,
                    "message": (
                        "The agentic workflow could not "
                        "complete this request."
                    ),
                },
            )

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
