"""create players table

Baseline recreated from the existing database schema; the original
5d30b51d46ac / 9bc1de56132c migration files were never committed.

Revision ID: 9bc1de56132c
Revises:
Create Date: 2026-09-15 21:46:38.248374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9bc1de56132c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'players',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('avatar', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('namecard', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_players_username'), 'players', ['username'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_players_username'), table_name='players')
    op.drop_table('players')
