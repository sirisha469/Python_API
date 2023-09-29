"""add content column to posts table

Revision ID: 9f3405a88b93
Revises: 60d656b67e81
Create Date: 2023-09-28 18:48:55.829025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f3405a88b93'
down_revision: Union[str, None] = '60d656b67e81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts', 
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
