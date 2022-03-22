"""empty message

Revision ID: aaef49cf57b2
Revises: 1ca76de8c486
Create Date: 2022-01-24 18:10:02.191858

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'aaef49cf57b2'
down_revision = '1ca76de8c486'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('day_picker', sa.Column('item_subtype_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'day_picker', ['item_subtype_id'])
    op.create_foreign_key(None, 'day_picker', 'item_subtype', ['item_subtype_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'day_picker', type_='foreignkey')
    op.drop_constraint(None, 'day_picker', type_='unique')
    op.drop_column('day_picker', 'item_subtype_id')
    # ### end Alembic commands ###
