"""add knowledge document metadata

Revision ID: 84e7b2c1a9f0
Revises: 261986073a62
Create Date: 2026-10-01

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "84e7b2c1a9f0"
down_revision: Union[str, Sequence[str], None] = "261986073a62"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "knowledge_documents",
        sa.Column("published_year", sa.Integer(), nullable=True),
    )
    op.add_column(
        "knowledge_documents",
        sa.Column("document_type", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "knowledge_documents",
        sa.Column("authority_level", sa.Integer(), nullable=True),
    )
    op.create_unique_constraint(
        "uq_knowledge_documents_filename",
        "knowledge_documents",
        ["filename"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_knowledge_documents_filename",
        "knowledge_documents",
        type_="unique",
    )
    op.drop_column("knowledge_documents", "authority_level")
    op.drop_column("knowledge_documents", "document_type")
    op.drop_column("knowledge_documents", "published_year")
