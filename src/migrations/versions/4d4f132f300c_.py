"""empty message

Revision ID: 4d4f132f300c
Revises: 59505c86aaa4
Create Date: 2022-01-24 19:25:44.588371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d4f132f300c'
down_revision = '59505c86aaa4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('item', 'item_type_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('item', 'item_subtype_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('item', 'item_subtype_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('item', 'item_type_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
