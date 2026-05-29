"""add content column to posts table

Revision ID: 8c0f055b146a
Revises: 9e7686b39465
Create Date: 2026-05-28 16:54:34.331434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c0f055b146a'
down_revision: Union[str, Sequence[str], None] = '9e7686b39465'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        'posts',
        'content'
    )
    pass
