from app.agents.state import AgentState


DANGEROUS_PHRASES = [
    "open the inverter",
    "touch the wires",
    "bypass the breaker",
    "disable the breaker",
    "rewire the system",
    "open the electrical panel",
]

OVERCONFIDENT_PHRASES = [
    "definitely faulty",
    "guaranteed savings",
    "guaranteed return",
    "100% certain",
    "will definitely",
]


def _format_measurement(
    value: object,
) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


def _missing_energy_usage_answer(
    energy_result: dict,
) -> str | None:
    latest = energy_result.get(
        "latest_consumption_kwh"
    )
    change = energy_result.get(
        "consumption_change_percent"
    )

    if latest is None:
        return (
            "No electricity-consumption records are currently "
            "available, so HelioSL cannot confirm that usage is "
            "increasing or determine why it may have changed. Add "
            "at least two consumption records to compare usage over "
            "time."
        )

    if change is None:
        return (
            "Your latest recorded electricity consumption is "
            f"{_format_measurement(latest)} kWh, but there is no "
            "usable preceding record for comparison. HelioSL "
            "therefore cannot confirm that usage is increasing or "
            "determine its cause yet."
        )

    return None


def _solar_performance_answer(
    energy_result: dict,
    trusted_sources_available: bool,
) -> str:
    latest = energy_result.get(
        "latest_generation_kwh"
    )
    change = energy_result.get(
        "generation_change_percent"
    )

    source_note = (
        " Trusted supporting information is available, but recorded "
        "generation measurements are still required to assess your "
        "system's performance."
        if trusted_sources_available
        else
        " No trusted knowledge source is currently available to "
        "verify a cause."
    )

    if latest is None:
        return (
            "No solar-generation records are currently available, "
            "so HelioSL cannot confirm that generation has dropped "
            "or determine its cause."
            + source_note
        )

    latest_text = _format_measurement(latest)

    if change is None:
        return (
            "Your latest recorded solar generation is "
            f"{latest_text} kWh, but there is no usable preceding "
            "record for comparison. HelioSL therefore cannot confirm "
            "that generation has dropped or determine its cause."
            + source_note
        )

    change_text = _format_measurement(abs(change))

    if change < 0:
        trend_text = (
            f"a {change_text}% decrease from the immediately "
            "preceding record"
        )
    elif change > 0:
        trend_text = (
            f"a {change_text}% increase from the immediately "
            "preceding record"
        )
    else:
        trend_text = (
            "no change from the immediately preceding record"
        )

    return (
        "Your latest recorded solar generation is "
        f"{latest_text} kWh, with {trend_text}. This observed change "
        "does not establish its cause."
        + source_note
        + " Have a qualified solar professional investigate any "
        "persistent or unexpected reduction."
    )


def _preliminary_financial_answer(
    state: AgentState,
) -> str:
    entities = state.get(
        "entities",
        {},
    )
    details: list[str] = []

    energy_kwh = entities.get(
        "energy_kwh"
    )
    capacity_kw = entities.get(
        "capacity_kw"
    )

    if energy_kwh is not None:
        details.append(
            "monthly energy use of "
            f"{_format_measurement(energy_kwh)} kWh"
        )

    if capacity_kw is not None:
        details.append(
            "a proposed capacity of "
            f"{_format_measurement(capacity_kw)} kW"
        )

    identified = "HelioSL "

    if details:
        identified = (
            "HelioSL identified "
            + " and ".join(details)
            + ", but "
        )

    suitability_text = (
        "cannot determine whether that capacity is suitable"
        if capacity_kw is not None
        else "cannot determine system suitability"
    )

    return (
        identified
        + suitability_text
        + " or estimate savings or payback. Verified tariff, "
        "installation-cost, site and "
        "applicable solar-scheme information is still required."
    )


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

    if any(
        phrase in answer_lower
        for phrase in DANGEROUS_PHRASES
    ):
        safety_passed = False

        notes.append(
            "Potentially unsafe electrical "
            "instruction detected."
        )

    if any(
        phrase in answer_lower
        for phrase in OVERCONFIDENT_PHRASES
    ):
        notes.append(
            "Potentially overconfident AI claim detected."
        )

    selected = state.get(
        "selected_agents",
        [],
    )

    knowledge_used = "knowledge" in selected

    sources = state.get(
        "sources",
        [],
    )

    if knowledge_used and not sources:
        notes.append(
            "Knowledge-based claims could not be "
            "verified against trusted sources."
        )

    financial_result = state.get(
        "financial_result",
        {},
    )

    financial_ready = financial_result.get(
        "financial_calculation_ready",
        False,
    )

    if (
        "financial" in selected
        and not financial_ready
    ):
        notes.append(
            "Financial recommendation is incomplete "
            "because verified planning inputs are missing."
        )

    energy_result = state.get(
        "energy_result",
        {},
    )

    if (
        "energy" in selected
        and energy_result.get(
            "latest_consumption_kwh"
        ) is None
        and energy_result.get(
            "latest_generation_kwh"
        ) is None
    ):
        notes.append(
            "Insufficient user energy history for "
            "a data-supported conclusion."
        )

    intent = state.get(
        "intent",
        "general",
    )

    if not safety_passed:
        final_answer = (
            "The generated recommendation contained "
            "potentially unsafe electrical guidance. "
            "Please consult a qualified solar or "
            "electrical professional."
        )

    elif intent == "energy_usage":
        energy_result = state.get(
            "energy_result",
            {},
        )

        final_answer = _missing_energy_usage_answer(
            energy_result
        )

        if final_answer is None:
            final_answer = draft

    elif intent == "solar_performance":
        energy_result = state.get(
            "energy_result",
            {},
        )
        generation_metrics_missing = (
            energy_result.get("latest_generation_kwh") is None
            or energy_result.get("generation_change_percent") is None
        )

        if generation_metrics_missing or not sources:
            final_answer = _solar_performance_answer(
                energy_result,
                bool(sources),
            )
        else:
            final_answer = draft

    elif knowledge_used and not sources and intent == "solar_scheme":
        final_answer = (
            "No trusted knowledge source is currently available "
            "to verify current solar-scheme rules, so HelioSL "
            "cannot recommend a scheme yet. Verified scheme "
            "terms, tariff information and your relevant energy "
            "data are required before making a recommendation."
        )

    elif (
        "financial" in state.get("selected_agents", [])
        and not financial_ready
    ):
        final_answer = _preliminary_financial_answer(
            state
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
        "Safety & Verification Agent performed "
        "Responsible AI compliance checks."
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
