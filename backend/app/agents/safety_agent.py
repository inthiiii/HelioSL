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


def _energy_usage_answer(
    energy_result: dict,
) -> str:
    latest = energy_result.get(
        "latest_consumption_kwh"
    )
    change = energy_result.get(
        "consumption_change_percent"
    )

    if latest is None:
        return (
            "### Energy trend\n"
            "No electricity-consumption records are currently "
            "available.\n\n"
            "### What is needed\n"
            "HelioSL cannot confirm that usage is increasing or "
            "determine its cause. Add at least two monthly consumption "
            "records before comparing usage over time."
        )

    if change is None:
        return (
            "### Energy trend\n"
            f"- Latest consumption: {_format_measurement(latest)} kWh\n"
            "- Month-to-month change: unavailable\n\n"
            "### Interpretation\n"
            "There is no usable preceding record, so HelioSL cannot "
            "confirm whether usage increased or determine why it may "
            "have changed."
        )

    if change > 0:
        change_text = (
            f"increased by {_format_measurement(change)}%"
        )
    elif change < 0:
        change_text = (
            "decreased by "
            f"{_format_measurement(abs(change))}%"
        )
    else:
        change_text = "did not change"

    trend = energy_result.get(
        "consumption_trend",
        "unavailable",
    )
    average = energy_result.get(
        "average_consumption_kwh"
    )

    average_line = ""

    if average is not None:
        average_line = (
            "- Recorded monthly average: "
            f"{_format_measurement(average)} kWh\n"
        )

    return (
        "### Energy trend\n"
        f"- Latest consumption: {_format_measurement(latest)} kWh\n"
        f"- Latest month-to-month change: {change_text}\n"
        f"- Overall recorded trend: {str(trend).replace('_', ' ')}\n"
        + average_line
        + "\n### Interpretation\n"
        "The records establish the direction of consumption, but they "
        "do not identify its cause. Changes in occupancy, operating "
        "hours, appliance use or billing-period length require separate "
        "evidence.\n\n"
        "### Next step\n"
        "Compare the relevant months against household or business "
        "activity and the original electricity bills."
    )


def _solar_performance_answer(
    energy_result: dict,
    trusted_sources_available: bool,
    weather_result: dict,
) -> str:
    latest = energy_result.get(
        "latest_generation_kwh"
    )
    change = energy_result.get(
        "generation_change_percent"
    )

    source_note = (
        "Trusted reference material was retrieved for general context, "
        "but it does not diagnose this installation."
        if trusted_sources_available
        else
        "No trusted knowledge source is currently available to verify "
        "a cause."
    )

    if weather_result.get("available"):
        location = weather_result.get(
            "location",
            "the saved location",
        )
        cloud_cover = weather_result.get(
            "cloud_cover_percent"
        )
        precipitation = weather_result.get(
            "precipitation_mm"
        )
        conditions: list[str] = []

        if cloud_cover is not None:
            conditions.append(
                f"{_format_measurement(cloud_cover)}% cloud cover"
            )

        if precipitation is not None:
            conditions.append(
                f"{_format_measurement(precipitation)} mm precipitation"
            )

        condition_text = (
            ", ".join(conditions)
            if conditions
            else "environmental conditions"
        )
        weather_note = (
            f"Current weather context for {location}: {condition_text}. "
            "These conditions may influence solar output, but current "
            "weather does not prove the cause of a historical change."
        )
    else:
        weather_note = (
            "Weather evidence was unavailable, so weather cannot be "
            "assessed as a contributor."
        )

    if latest is None:
        return (
            "### Solar trend\n"
            "No solar-generation records are currently available.\n\n"
            "### Evidence limits\n"
            "HelioSL cannot confirm that generation has dropped or determine "
            "its cause. "
            + source_note
        )

    latest_text = _format_measurement(latest)

    if change is None:
        return (
            "### Solar trend\n"
            f"- Latest generation: {latest_text} kWh\n"
            "- Month-to-month change: unavailable\n\n"
            "### Evidence limits\n"
            "There is no usable preceding record, so HelioSL cannot "
            "confirm that generation has dropped or determine its cause. "
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
        "### Solar trend\n"
        f"- Latest generation: {latest_text} kWh\n"
        f"- Latest month-to-month change: {trend_text}\n\n"
        "### Evidence and interpretation\n"
        "- The measured change does not establish its cause.\n"
        f"- {weather_note}\n"
        f"- {source_note}\n\n"
        "### Recommended action\n"
        "If the reduction persists, compare inverter monitoring and "
        "maintenance records and ask a qualified solar professional "
        "to inspect the system."
    )


def _preliminary_financial_answer(
    state: AgentState,
) -> str:
    entities = state.get(
        "entities",
        {},
    )
    financial = state.get(
        "financial_result",
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
            "- User-provided monthly energy use: "
            f"{_format_measurement(energy_kwh)} kWh"
        )
    else:
        profile_energy = financial.get(
            "monthly_consumption_kwh"
        )

        if profile_energy is not None:
            details.append(
                "- Recorded monthly average consumption: "
                f"{_format_measurement(profile_energy)} kWh"
            )

    if capacity_kw is not None:
        details.append(
            "- Capacity stated in the question: "
            f"{_format_measurement(capacity_kw)} kW"
        )
    else:
        recorded_capacity = financial.get(
            "requested_capacity_kw"
        )

        if recorded_capacity is not None:
            details.append(
                "- Recorded solar-system capacity: "
                f"{_format_measurement(recorded_capacity)} kW"
            )

    suitability_text = (
        "cannot determine whether that capacity is suitable"
        if capacity_kw is not None
        else "cannot determine system suitability"
    )

    context = (
        "\n".join(details)
        if details
        else "- No usable consumption or capacity input was available."
    )

    return (
        "### Available planning context\n"
        + context
        + "\n\n### Conclusion\nHelioSL "
        + suitability_text
        + " or estimate savings or payback from the available evidence."
        "\n\n### Required verified inputs\n"
        "- Current import tariff and export compensation\n"
        "- Installation cost\n"
        "- Site-specific solar yield, roof and shading assessment\n"
        "- Applicable solar-scheme terms"
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

        final_answer = _energy_usage_answer(
            energy_result
        )

    elif intent == "solar_performance":
        energy_result = state.get(
            "energy_result",
            {},
        )
        final_answer = _solar_performance_answer(
            energy_result,
            bool(sources),
            state.get("weather_result", {}),
        )

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
