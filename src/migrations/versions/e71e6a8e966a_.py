"""empty message

Revision ID: e71e6a8e966a
Revises: eeef3aab2951
Create Date: 2022-06-17 15:22:04.432463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e71e6a8e966a'
down_revision = 'eeef3aab2951'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('voucher', sa.Column('counter', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('voucher', 'counter')
    # ### end Alembic commands ###
