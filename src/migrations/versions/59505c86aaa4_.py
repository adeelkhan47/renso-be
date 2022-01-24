"""empty message

Revision ID: 59505c86aaa4
Revises: a3d377e8931f
Create Date: 2022-01-24 19:20:44.244684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59505c86aaa4'
down_revision = 'a3d377e8931f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('day_picker', 'item_subtype_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('day_picker', 'item_subtype_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
