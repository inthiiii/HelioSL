from typing import Any


def add_user_context(
    entities: dict[str, Any],
    district: str | None,
) -> dict[str, Any]:
    contextualized = dict(entities)

    if (
        not contextualized.get("location")
        and district
    ):
        contextualized["location"] = district

    return contextualized
