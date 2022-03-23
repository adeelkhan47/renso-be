"""empty message

Revision ID: 04801025b12f
Revises: 2a228afa378b
Create Date: 2022-03-22 01:34:19.945749

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '04801025b12f'
down_revision = '2a228afa378b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('cost', sa.Float(), nullable=True))
    op.drop_column('booking', 'discount')
    op.drop_column('booking', 'location')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('location', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('booking', sa.Column('discount', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('booking', 'cost')
    # ### end Alembic commands ###