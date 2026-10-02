import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent


def load_dataset(
    filename: str,
) -> list[dict]:

    path = (
        BASE_DIR
        / "datasets"
        / filename
    )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def save_results(
    filename: str,
    data: Any,
) -> None:

    path = (
        BASE_DIR
        / "results"
        / filename
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )
