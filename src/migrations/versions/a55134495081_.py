"""empty message

Revision ID: a55134495081
Revises: cb047b3934d5
Create Date: 2022-04-14 03:33:06.767903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a55134495081'
down_revision = 'cb047b3934d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_index(op.f('ix_logo_updated_at'), 'logo', ['updated_at'], unique=False)
    op.create_index(op.f('ix_logo_user_id'), 'logo', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_logo_user_id'), table_name='logo')
    op.drop_index(op.f('ix_logo_updated_at'), table_name='logo')
    op.drop_table('logo')
    # ### end Alembic commands ###
