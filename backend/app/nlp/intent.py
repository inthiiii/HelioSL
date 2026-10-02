def classify_intent(
    text: str,
) -> str:

    query = text.lower()

    if any(
        word in query
        for word in [
            "bill",
            "cost",
            "price",
            "pay",
            "saving",
        ]
    ):
        return "financial"

    if any(
        word in query
        for word in [
            "generation",
            "generate",
            "output",
            "production",
            "performance",
        ]
    ):
        return "solar_performance"

    if any(
        word in query
        for word in [
            "consumption",
            "usage",
            "electricity use",
        ]
    ):
        return "energy_usage"

    if any(
        word in query
        for word in [
            "scheme",
            "net metering",
            "net accounting",
            "net plus",
        ]
    ):
        return "solar_scheme"

    if any(
        word in query
        for word in [
            "install",
            "capacity",
            "kw",
            "solar system",
            "solar suitability",
            "suitability of solar",
            "suitable for",
        ]
    ):
        return "solar_planning"

    return "general"
