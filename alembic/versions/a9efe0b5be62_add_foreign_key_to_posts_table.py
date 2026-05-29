"""add foreign key to posts table

Revision ID: a9efe0b5be62
Revises: 3ff548b8eea8
Create Date: 2026-05-28 17:48:35.124053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9efe0b5be62'
down_revision: Union[str, Sequence[str], None] = '3ff548b8eea8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )

    op.create_foreign_key(
        'posts_users_fk', 
        source_table='posts', 
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column(table_name='posts', column_name='owner_id')

    pass
