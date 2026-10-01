"""add knowledge effective date

Revision ID: 9d2f6a8c4b11
Revises: 84e7b2c1a9f0
Create Date: 2026-10-01

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9d2f6a8c4b11"
down_revision: Union[str, Sequence[str], None] = "84e7b2c1a9f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "knowledge_documents",
        sa.Column("effective_date", sa.Date(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("knowledge_documents", "effective_date")
