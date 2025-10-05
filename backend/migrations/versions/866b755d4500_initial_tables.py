"""Initial tables

Revision ID: 866b755d4500
Revises: 9b49bab197b7
Create Date: 2025-09-04 04:01:12.030516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '866b755d4500'
down_revision: Union[str, None] = '9b49bab197b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
