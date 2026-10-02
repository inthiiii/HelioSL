from app.security.prompt_guard import (
    detect_prompt_injection,
)


TRUSTED_ORGANIZATIONS = {
    "PUCSL",
    "CEB",
    "LECO",
    "SLSEA",
    "Ministry of Energy",
    "Public Utilities Commission of Sri Lanka",
    "Ceylon Electricity Board",
    "Lanka Electricity Company",
    "Sri Lanka Sustainable Energy Authority",
    "Parliament of Sri Lanka",
}


def evaluate_source_trust(
    organization: str | None,
) -> dict:

    if not organization:
        return {
            "trusted": False,
            "reason": "Missing organization metadata",
        }

    trusted = (
        organization.strip()
        in TRUSTED_ORGANIZATIONS
    )

    return {
        "trusted": trusted,
        "reason": (
            "Recognized authoritative source"
            if trusted
            else "Source is not on the trusted authority list"
        ),
    }


def sanitize_retrieved_content(
    content: str,
) -> dict:

    injection = detect_prompt_injection(
        content
    )

    return {
        "safe": not injection[
            "is_suspicious"
        ],
        "content": (
            content
            if not injection["is_suspicious"]
            else ""
        ),
        "matches": injection["matches"],
    }
