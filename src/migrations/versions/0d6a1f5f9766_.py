"""empty message

Revision ID: 0d6a1f5f9766
Revises: 626e43f00257
Create Date: 2022-06-30 01:54:43.728140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d6a1f5f9766'
down_revision = '626e43f00257'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('bate_number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('company', 'bate_number')
    # ### end Alembic commands ###
