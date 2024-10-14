"""added booster model

Revision ID: 88844fce4909
Revises: 
Create Date: 2024-10-14 23:25:10.942762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88844fce4909'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booster',
    sa.Column('userid', sa.BigInteger(), nullable=False),
    sa.Column('boosting_since', sa.DateTime(), nullable=True),
    sa.Column('expired_since', sa.DateTime(), nullable=True),
    sa.Column('isboosting', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('userid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booster')
    # ### end Alembic commands ###
