"""add role to users

Revision ID: 7c90eb92dd94
Revises: 3403b2d17bec
Create Date: 2026-09-20 14:21:49.987934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c90eb92dd94'
down_revision: Union[str, Sequence[str], None] = '3403b2d17bec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=50),
            nullable=False,
            server_default="user",
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    # Defaults above safely backfill existing rows. New values are supplied by
    # the application, so the database does not need permanent defaults.
    op.alter_column("users", "role", server_default=None)
    op.alter_column("users", "is_active", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "is_active")
    op.drop_column("users", "role")
