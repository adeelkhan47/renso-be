"""empty message

Revision ID: 3451dd176991
Revises: 6241905dfd8c
Create Date: 2022-04-15 22:43:08.110485

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3451dd176991'
down_revision = '6241905dfd8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('front_end_configs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('logo', sa.String(), nullable=False),
    sa.Column('front_end_url', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_front_end_configs_updated_at'), 'front_end_configs', ['updated_at'], unique=False)
    op.create_index(op.f('ix_front_end_configs_user_id'), 'front_end_configs', ['user_id'], unique=False)
    op.drop_index('ix_logo_updated_at', table_name='logo')
    op.drop_index('ix_logo_user_id', table_name='logo')
    op.drop_table('logo')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logo',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='logo_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='logo_pkey')
    )
    op.create_index('ix_logo_user_id', 'logo', ['user_id'], unique=False)
    op.create_index('ix_logo_updated_at', 'logo', ['updated_at'], unique=False)
    op.drop_index(op.f('ix_front_end_configs_user_id'), table_name='front_end_configs')
    op.drop_index(op.f('ix_front_end_configs_updated_at'), table_name='front_end_configs')
    op.drop_table('front_end_configs')
    # ### end Alembic commands ###