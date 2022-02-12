"""empty message

Revision ID: de575b7d1b18
Revises: 64d68f3411e3
Create Date: 2022-02-12 16:00:22.619064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de575b7d1b18'
down_revision = '64d68f3411e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('season',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('price_factor', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_season_updated_at'), 'season', ['updated_at'], unique=False)
    op.create_table('season_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('season_id', sa.Integer(), nullable=False),
    sa.Column('item_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_type_id'], ['item_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['season_id'], ['season.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_season_type_updated_at'), 'season_type', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_season_type_updated_at'), table_name='season_type')
    op.drop_table('season_type')
    op.drop_index(op.f('ix_season_updated_at'), table_name='season')
    op.drop_table('season')
    # ### end Alembic commands ###
