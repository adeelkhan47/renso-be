"""empty message

Revision ID: 65c38d0f546f
Revises: 7a3fa5b5eb49
Create Date: 2022-06-10 17:18:41.206300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65c38d0f546f'
down_revision = '7a3fa5b5eb49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email_text',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('text', sa.String(length=1200), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_email_text_updated_at'), 'email_text', ['updated_at'], unique=False)
    op.create_index(op.f('ix_email_text_user_id'), 'email_text', ['user_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_email_text_user_id'), table_name='email_text')
    op.drop_index(op.f('ix_email_text_updated_at'), table_name='email_text')
    op.drop_table('email_text')
    # ### end Alembic commands ###