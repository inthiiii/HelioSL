"""add vector embeddings to knowledge chunks

Revision ID: 261986073a62
Revises: 63565f62c0ff
Create Date: 2026-09-29 10:37:04.943169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = '261986073a62'
down_revision: Union[str, Sequence[str], None] = '63565f62c0ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.add_column(
        "knowledge_chunks",
        sa.Column(
            "embedding",
            Vector(768),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "knowledge_chunks",
        "embedding",
    )
