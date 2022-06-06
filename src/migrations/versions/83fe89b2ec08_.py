"""empty message

Revision ID: 83fe89b2ec08
Revises: 4dc88d5c96ad
Create Date: 2022-06-06 20:38:09.200293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83fe89b2ec08'
down_revision = '4dc88d5c96ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restricted_dates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('item_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_type_id'], ['item_type.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_restricted_dates_item_type_id'), 'restricted_dates', ['item_type_id'], unique=False)
    op.create_index(op.f('ix_restricted_dates_updated_at'), 'restricted_dates', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_restricted_dates_updated_at'), table_name='restricted_dates')
    op.drop_index(op.f('ix_restricted_dates_item_type_id'), table_name='restricted_dates')
    op.drop_table('restricted_dates')
    # ### end Alembic commands ###