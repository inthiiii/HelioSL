from sqlalchemy.orm import Session

from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.agents.energy_agent import (
    run_energy_agent,
)

from app.agents.financial_agent import (
    run_financial_agent,
)

from app.agents.knowledge_agent import (
    run_knowledge_agent,
)

from app.agents.orchestrator import (
    orchestrator_agent,
)

from app.agents.safety_agent import (
    safety_agent,
)

from app.agents.state import AgentState

from app.llm.client import (
    get_llm_client,
)


def build_agent_graph(
    db: Session,
):

    workflow = StateGraph(
        AgentState
    )

    def energy_node(
        state: AgentState,
    ) -> AgentState:

        if "energy" not in state.get(
            "selected_agents",
            [],
        ):
            return {
                **state,
                "trace": [
                    *state.get("trace", []),
                    "Energy Intelligence Agent skipped "
                    "by the orchestrator.",
                ],
            }

        return run_energy_agent(
            state,
            db,
        )

    def knowledge_node(
        state: AgentState,
    ) -> AgentState:

        if "knowledge" not in state.get(
            "selected_agents",
            [],
        ):
            return {
                **state,
                "trace": [
                    *state.get("trace", []),
                    "Renewable Energy Knowledge Agent "
                    "skipped by the orchestrator.",
                ],
            }

        return run_knowledge_agent(
            state,
            db,
        )

    def financial_node(
        state: AgentState,
    ) -> AgentState:

        if "financial" not in state.get(
            "selected_agents",
            [],
        ):
            return {
                **state,
                "trace": [
                    *state.get("trace", []),
                    "Financial and Solar Planning Agent "
                    "skipped by the orchestrator.",
                ],
            }

        return run_financial_agent(
            state
        )

    def generate_node(
        state: AgentState,
    ) -> AgentState:

        llm = get_llm_client()

        prompt = f"""
User question:
{state.get("original_query")}

Intent:
{state.get("intent")}

Energy Agent:
{state.get("energy_result", {})}

Knowledge Agent:
{state.get("knowledge_result", {})}

Financial & Solar Planning Agent:
{state.get("financial_result", {})}

Generate a concise renewable-energy decision-support response.

Rules:
- Never invent missing information.
- Distinguish calculations from verified facts.
- If official information is unavailable, say so.
- Do not give dangerous electrical repair instructions.
- Financial estimates must clearly state assumptions.
"""

        answer = llm.generate(
            prompt=prompt,
            system_prompt=(
                "You are HelioSL, an Agentic AI "
                "renewable-energy decision-support "
                "platform for Sri Lanka."
            ),
        )

        trace = list(
            state.get(
                "trace",
                [],
            )
        )

        trace.append(
            "LLM synthesis combined the "
            "specialist-agent outputs."
        )

        return {
            **state,
            "draft_answer":
                answer,

            "trace":
                trace,
        }

    workflow.add_node(
        "orchestrator",
        orchestrator_agent,
    )

    workflow.add_node(
        "energy",
        energy_node,
    )

    workflow.add_node(
        "knowledge",
        knowledge_node,
    )

    workflow.add_node(
        "financial",
        financial_node,
    )

    workflow.add_node(
        "generate",
        generate_node,
    )

    workflow.add_node(
        "safety",
        safety_agent,
    )

    workflow.add_edge(
        START,
        "orchestrator",
    )

    workflow.add_edge(
        "orchestrator",
        "energy",
    )

    workflow.add_edge(
        "energy",
        "knowledge",
    )

    workflow.add_edge(
        "knowledge",
        "financial",
    )

    workflow.add_edge(
        "financial",
        "generate",
    )

    workflow.add_edge(
        "generate",
        "safety",
    )

    workflow.add_edge(
        "safety",
        END,
    )

    return workflow.compile()
