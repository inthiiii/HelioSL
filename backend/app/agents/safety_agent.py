from app.agents.state import AgentState


DANGEROUS_PHRASES = [
    "open the inverter",
    "touch the wires",
    "bypass the breaker",
    "disable the breaker",
    "rewire the system",
    "open the electrical panel",
]


def safety_agent(
    state: AgentState,
) -> AgentState:

    draft = state.get(
        "draft_answer",
        "",
    )

    answer_lower = draft.lower()

    notes: list[str] = []

    safety_passed = True

    for phrase in DANGEROUS_PHRASES:
        if phrase in answer_lower:
            safety_passed = False

            notes.append(
                "Potentially unsafe electrical "
                "instruction detected."
            )

    knowledge_used = (
        "knowledge"
        in state.get(
            "selected_agents",
            [],
        )
    )

    sources = state.get(
        "sources",
        [],
    )

    if knowledge_used and not sources:
        notes.append(
            "No trusted retrieval source was "
            "available for the knowledge-based "
            "part of this response."
        )

    financial_result = state.get(
        "financial_result",
        {},
    )

    if (
        "financial"
        in state.get(
            "selected_agents",
            [],
        )
        and not financial_result.get(
            "financial_calculation_ready",
            False,
        )
    ):
        notes.append(
            "Financial result is preliminary "
            "because verified tariff or cost "
            "information is unavailable."
        )

    if not safety_passed:
        final_answer = (
            "The generated recommendation contained "
            "potentially unsafe electrical guidance. "
            "Please consult a qualified solar or "
            "electrical professional."
        )

    else:
        final_answer = draft

    trace = list(
        state.get(
            "trace",
            [],
        )
    )

    trace.append(
        "Safety & Verification Agent reviewed "
        "evidence, financial limitations and "
        "electrical safety."
    )

    return {
        **state,
        "safety_passed":
            safety_passed,

        "safety_notes":
            notes,

        "final_answer":
            final_answer,

        "trace":
            trace,
    }