"""enable pgvector extension

Revision ID: 63565f62c0ff
Revises: b05b078256d0
Create Date: 2026-09-29 10:22:30.379637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63565f62c0ff'
down_revision: Union[str, Sequence[str], None] = 'b05b078256d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS vector")
