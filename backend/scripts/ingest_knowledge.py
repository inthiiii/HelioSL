from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from sqlalchemy import select


BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import SessionLocal  # noqa: E402
from app.models.knowledge import (  # noqa: E402
    KnowledgeChunk,
    KnowledgeDocument,
)
from app.rag.chunker import chunk_text  # noqa: E402
from app.rag.embeddings import create_embedding  # noqa: E402
from app.rag.loader import load_document  # noqa: E402


SUPPORTED_SUFFIXES = {".pdf", ".txt", ".md"}
REQUIRED_METADATA_FIELDS = {
    "filename",
    "title",
    "organization",
    "published_year",
    "effective_date",
    "document_type",
    "authority_level",
    "source_url",
}
EMBEDDING_DIMENSION = 768


def load_metadata(path: Path) -> dict[str, dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(raw, list):
        raise ValueError("metadata.json must contain a JSON array")

    metadata: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Metadata item {index} must be an object")

        missing = REQUIRED_METADATA_FIELDS - item.keys()
        if missing:
            fields = ", ".join(sorted(missing))
            raise ValueError(f"Metadata item {index} is missing: {fields}")

        filename = item["filename"]
        if not isinstance(filename, str) or not filename.strip():
            raise ValueError(f"Metadata item {index} has an invalid filename")
        if filename in metadata:
            raise ValueError(f"Duplicate metadata for filename: {filename}")

        authority_level = item["authority_level"]
        if authority_level not in {1, 2, 3}:
            raise ValueError(
                f"Invalid authority_level for {filename}: {authority_level}"
            )

        metadata[filename] = item

    return metadata


def discover_documents(directory: Path) -> list[Path]:
    return sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def metadata_values(item: dict[str, Any]) -> dict[str, Any]:
    effective_date = item["effective_date"]
    if effective_date is not None:
        effective_date = date.fromisoformat(effective_date)

    return {
        "filename": item["filename"],
        "title": item["title"],
        "organization": item["organization"],
        "published_year": item["published_year"],
        "effective_date": effective_date,
        "document_type": item["document_type"],
        "authority_level": item["authority_level"],
        "source_url": item["source_url"],
    }


def validate_document_metadata(
    documents: list[Path],
    metadata: dict[str, dict[str, Any]],
) -> None:
    filenames = {document.name for document in documents}
    missing = filenames - metadata.keys()
    unknown = metadata.keys() - filenames

    if missing:
        raise ValueError(
            "Documents without metadata: " + ", ".join(sorted(missing))
        )
    if unknown:
        raise ValueError(
            "Metadata without a document: " + ", ".join(sorted(unknown))
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Embed trusted documents and store them in PostgreSQL/pgvector."
    )
    parser.add_argument(
        "--documents-dir",
        type=Path,
        default=BACKEND_DIR / "knowledge" / "documents",
    )
    parser.add_argument(
        "--metadata-file",
        type=Path,
        default=BACKEND_DIR / "knowledge" / "metadata.json",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Re-embed documents that already exist (matched by filename).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metadata = load_metadata(args.metadata_file)
    documents = discover_documents(args.documents_dir)
    validate_document_metadata(documents, metadata)

    if not documents:
        raise RuntimeError(f"No supported documents found in {args.documents_dir}")

    print(f"Found {len(documents)} document(s).")
    print(f"Loaded {len(metadata)} metadata record(s).")

    total_chunks = 0
    inserted_documents = 0
    skipped_documents = 0
    checked_dimension = False

    with SessionLocal() as db:
        for document_path in documents:
            item = metadata[document_path.name]
            existing = db.scalar(
                select(KnowledgeDocument).where(
                    KnowledgeDocument.filename == document_path.name
                )
            )

            if existing is not None and not args.replace:
                for field, value in metadata_values(item).items():
                    setattr(existing, field, value)
                print(f"SKIP {document_path.name} (already ingested)")
                skipped_documents += 1
                continue

            if existing is not None:
                db.delete(existing)
                db.flush()

            print(f"LOAD {document_path.name}")
            text = load_document(document_path)
            chunks = chunk_text(text)
            if not chunks:
                raise ValueError(f"No extractable text found in {document_path.name}")

            document = KnowledgeDocument(**metadata_values(item))
            db.add(document)
            db.flush()

            for chunk_index, content in enumerate(chunks):
                embedding = create_embedding(content)
                if not checked_dimension:
                    print(f"Embedding dimension: {len(embedding)}")
                    checked_dimension = True
                if len(embedding) != EMBEDDING_DIMENSION:
                    raise ValueError(
                        "Embedding dimension mismatch: "
                        f"expected {EMBEDDING_DIMENSION}, got {len(embedding)}"
                    )

                db.add(
                    KnowledgeChunk(
                        document_id=document.id,
                        chunk_index=chunk_index,
                        content=content,
                        embedding=embedding,
                    )
                )

            db.commit()
            inserted_documents += 1
            total_chunks += len(chunks)
            print(f"DONE {document_path.name}: {len(chunks)} chunk(s)")

        db.commit()

    print("Ingestion complete.")
    print(f"Documents inserted: {inserted_documents}")
    print(f"Documents skipped: {skipped_documents}")
    print(f"Chunks inserted: {total_chunks}")


if __name__ == "__main__":
    main()
