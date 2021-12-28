"""empty message

Revision ID: 6a1cceb8559a
Revises: 278c7833cb6a
Create Date: 2021-12-23 23:53:12.196923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a1cceb8559a'
down_revision = '278c7833cb6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('item_type_maintenance_key', 'item_type', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('item_type_maintenance_key', 'item_type', ['maintenance'])
    # ### end Alembic commands ###