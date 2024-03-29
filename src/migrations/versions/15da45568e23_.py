"""empty message

Revision ID: 15da45568e23
Revises: 335a3bcd06b3
Create Date: 2022-07-17 14:44:47.611825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15da45568e23'
down_revision = '335a3bcd06b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('False'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_deleted')
    # ### end Alembic commands ###
