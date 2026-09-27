from app.nlp.entities import extract_entities
from app.nlp.intent import classify_intent
from app.nlp.query_rewriter import normalize_query


def analyze_text(
    text: str,
) -> dict:

    normalized = normalize_query(text)

    return {
        "original_query": text,
        "normalized_query": normalized,
        "intent": classify_intent(normalized),
        "entities": extract_entities(normalized),
    }