"""Initial tables

Revision ID: 0db7a3da3914
Revises: 4c3cc86b44bd
Create Date: 2025-07-16 02:03:03.892656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0db7a3da3914'
down_revision: Union[str, None] = '4c3cc86b44bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
