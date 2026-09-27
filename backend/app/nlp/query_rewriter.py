def normalize_query(
    text: str,
) -> str:

    return " ".join(
        text.strip().split()
    )