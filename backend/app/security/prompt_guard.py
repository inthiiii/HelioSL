import re


SUSPICIOUS_PATTERNS = [
    r"ignore (all|any|the) previous instructions",
    r"ignore your previous instructions",
    r"forget your instructions",
    r"reveal (the )?system prompt",
    r"show (me )?your system prompt",
    r"developer mode",
    r"jailbreak",
    r"bypass (your|the) rules",
    r"act as if you have no restrictions",
    r"override (the )?system",
    r"reveal hidden instructions",
]


def detect_prompt_injection(
    text: str,
) -> dict:

    lowered = text.lower()

    detected: list[str] = []

    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(
            pattern,
            lowered,
            flags=re.IGNORECASE,
        ):
            detected.append(pattern)

    return {
        "is_suspicious": bool(detected),
        "matches": detected,
    }