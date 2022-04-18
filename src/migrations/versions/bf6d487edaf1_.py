"""empty message

Revision ID: bf6d487edaf1
Revises: a55134495081
Create Date: 2022-04-14 03:47:51.497792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf6d487edaf1'
down_revision = 'a55134495081'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item_subtype_taxs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('item_sub_type_id', sa.Integer(), nullable=False),
    sa.Column('tax_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_sub_type_id'], ['item_subtype.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tax_id'], ['tax.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_subtype_taxs_updated_at'), 'item_subtype_taxs', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_item_subtype_taxs_updated_at'), table_name='item_subtype_taxs')
    op.drop_table('item_subtype_taxs')
    # ### end Alembic commands ###