import re


SRI_LANKAN_DISTRICTS = [
    "colombo",
    "gampaha",
    "kalutara",
    "kandy",
    "matale",
    "nuwara eliya",
    "galle",
    "matara",
    "hambantota",
    "jaffna",
    "kilinochchi",
    "mannar",
    "vavuniya",
    "mullaitivu",
    "batticaloa",
    "ampara",
    "trincomalee",
    "kurunegala",
    "puttalam",
    "anuradhapura",
    "polonnaruwa",
    "badulla",
    "monaragala",
    "ratnapura",
    "kegalle",
]


def extract_entities(
    text: str,
) -> dict:

    query = text.lower()

    entities = {
        "location": None,
        "capacity_kw": None,
        "energy_kwh": None,
    }

    for district in SRI_LANKAN_DISTRICTS:
        if district in query:
            entities["location"] = district.title()
            break

    capacity_match = re.search(
        r"(\d+(?:\.\d+)?)\s*kw\b",
        query,
    )

    if capacity_match:
        entities["capacity_kw"] = float(
            capacity_match.group(1)
        )

    energy_match = re.search(
        r"(\d+(?:\.\d+)?)\s*kwh\b",
        query,
    )

    if energy_match:
        entities["energy_kwh"] = float(
            energy_match.group(1)
        )

    return entities