"""add product

Revision ID: c29415aee3cf
Revises: d0dba177c834
Create Date: 2023-08-19 22:31:50.083638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c29415aee3cf'
down_revision: Union[str, None] = 'd0dba177c834'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('sku', sa.String(length=255), nullable=False),
    sa.Column('version_number', sa.Integer(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('sku')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    # ### end Alembic commands ###
