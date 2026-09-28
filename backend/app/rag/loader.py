from pathlib import Path

from pypdf import PdfReader


def load_pdf(path: Path) -> str:
    reader = PdfReader(path)

    pages: list[str] = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def load_text(path: Path) -> str:
    return path.read_text(
        encoding="utf-8"
    )


def load_document(path: Path) -> str:
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return load_pdf(path)

    if suffix in {".txt", ".md"}:
        return load_text(path)

    raise ValueError(
        f"Unsupported document type: {suffix}"
    )