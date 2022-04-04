"""empty message

Revision ID: 3631258ea2a4
Revises: 8107e782105f
Create Date: 2022-04-04 23:12:50.870699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3631258ea2a4'
down_revision = '8107e782105f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('image', sa.String(length=500), nullable=False))
    op.drop_column('item', 'images')
    op.add_column('item_subtype', sa.Column('image', sa.String(length=500), nullable=False))
    op.add_column('item_type', sa.Column('image', sa.String(length=500), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item_type', 'image')
    op.drop_column('item_subtype', 'image')
    op.add_column('item', sa.Column('images', sa.VARCHAR(length=500), autoincrement=False, nullable=False))
    op.drop_column('item', 'image')
    # ### end Alembic commands ###