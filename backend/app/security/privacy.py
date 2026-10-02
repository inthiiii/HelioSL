import re


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

JWT_PATTERN = re.compile(
    r"\beyJ[A-Za-z0-9_-]+\."
    r"[A-Za-z0-9_-]+\."
    r"[A-Za-z0-9_-]+\b"
)


def redact_sensitive_data(
    text: str,
) -> str:

    text = EMAIL_PATTERN.sub(
        "[REDACTED_EMAIL]",
        text,
    )

    text = JWT_PATTERN.sub(
        "[REDACTED_TOKEN]",
        text,
    )

    return text
