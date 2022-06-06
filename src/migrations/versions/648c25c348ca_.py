"""empty message

Revision ID: 648c25c348ca
Revises: 83fe89b2ec08
Create Date: 2022-06-06 22:00:01.398532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '648c25c348ca'
down_revision = '83fe89b2ec08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('restricted_dates', 'end_date',
               existing_type=sa.DATE(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('restricted_dates', 'end_date',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###
