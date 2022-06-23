"""empty message

Revision ID: eeef3aab2951
Revises: 81c25631802b
Create Date: 2022-06-17 15:08:04.093326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeef3aab2951'
down_revision = '81c25631802b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item_subtype', sa.Column('description', sa.String(), nullable=True))
    op.add_column('item_subtype', sa.Column('show_description', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item_subtype', 'show_description')
    op.drop_column('item_subtype', 'description')
    # ### end Alembic commands ###