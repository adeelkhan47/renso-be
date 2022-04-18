"""empty message

Revision ID: 84eb3eaa2bf1
Revises: 5427983a3862
Create Date: 2022-04-13 03:22:24.633056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84eb3eaa2bf1'
down_revision = '5427983a3862'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item_subtype', sa.Column('price', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item_subtype', 'price')
    # ### end Alembic commands ###