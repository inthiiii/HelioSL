import re
import unicodedata


SUSPICIOUS_PATTERNS = [
    (
        "instruction_override",
        r"\b(?:ignore|forget|disregard|override)\b.{0,100}"
        r"\b(?:previous|earlier|prior|existing|system|developer|all|your)\b"
        r".{0,100}\b(?:instructions?|restrictions?|rules?|guardrails?|prompts?)\b",
    ),
    (
        "restriction_bypass",
        r"\b(?:bypass|disable|remove|circumvent)\b.{0,80}"
        r"\b(?:security|safety|restrictions?|rules?|guardrails?)\b",
    ),
    (
        "unrestricted_roleplay",
        r"\b(?:act|pretend|behave)\b.{0,80}"
        r"\b(?:no|without)\b.{0,40}"
        r"\b(?:restrictions?|safety|rules?|guardrails?)\b",
    ),
    (
        "known_attack_term",
        r"\b(?:developer mode|jailbreak)\b",
    ),
    (
        "customer_data_exfiltration",
        r"\b(?:reveal|show|print|display|dump|expose|return|provide|give|list)\b"
        r".{0,140}\b(?:customer|user)\b.{0,30}\b(?:private )?data\b",
    ),
]


DISCLOSURE_VERB = re.compile(
    r"\b(?:reveal|show|print|display|dump|expose|return|provide|give|list|repeat|write out|tell me)\b"
)


SENSITIVE_TARGET = re.compile(
    r"\b(?:"
    r"system prompts?|developer (?:prompts?|messages?|instructions?)|"
    r"hidden (?:prompts?|messages?|instructions?)|"
    r"internal (?:prompts?|messages?|instructions?)|"
    r"tool (?:prompts?|messages?|instructions?)|"
    r"security configuration|private (?:user|customer) data|"
    r"complete system prompt|every message"
    r")\b"
)


def normalize_prompt_text(text: str) -> str:
    normalized = unicodedata.normalize(
        "NFKC",
        text,
    ).casefold()
    normalized = re.sub(
        r"[\u200b-\u200f\u2060\ufeff]",
        "",
        normalized,
    )
    return re.sub(
        r"\s+",
        " ",
        normalized,
    ).strip()


def detect_prompt_injection(
    text: str,
) -> dict:
    normalized = normalize_prompt_text(text)
    detected: list[str] = []

    for name, pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, normalized):
            detected.append(name)

    if (
        DISCLOSURE_VERB.search(normalized)
        and SENSITIVE_TARGET.search(normalized)
    ):
        detected.append(
            "sensitive_instruction_disclosure"
        )

    return {
        "is_suspicious": bool(detected),
        "matches": list(dict.fromkeys(detected)),
    }
