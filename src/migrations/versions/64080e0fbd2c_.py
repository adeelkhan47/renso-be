"""empty message

Revision ID: 64080e0fbd2c
Revises: ec79d42ef913
Create Date: 2022-01-25 00:12:08.995093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64080e0fbd2c'
down_revision = 'ec79d42ef913'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('day_picker_item_type_id_key', 'day_picker', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('day_picker_item_type_id_key', 'day_picker', ['item_type_id'])
    # ### end Alembic commands ###
