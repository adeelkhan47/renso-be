"""empty message

Revision ID: 5427983a3862
Revises: d6f4673bbdfd
Create Date: 2022-04-13 03:22:16.405201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5427983a3862'
down_revision = 'd6f4673bbdfd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item_subtype', 'price')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item_subtype', sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
