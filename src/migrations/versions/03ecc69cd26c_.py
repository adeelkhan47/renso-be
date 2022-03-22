"""empty message

Revision ID: 03ecc69cd26c
Revises: 83a78bbf887c
Create Date: 2021-12-25 23:28:46.938672

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '03ecc69cd26c'
down_revision = '83a78bbf887c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image', sa.String(), nullable=True))
    op.add_column('user', sa.Column('gender', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'gender')
    op.drop_column('user', 'image')
    # ### end Alembic commands ###
