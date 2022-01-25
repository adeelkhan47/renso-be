"""empty message

Revision ID: 1ca76de8c486
Revises: a09a779a8127
Create Date: 2022-01-24 18:00:57.430442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ca76de8c486'
down_revision = 'a09a779a8127'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item_subtype',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.String(), nullable=False),
    sa.Column('person', sa.Integer(), nullable=False),
    sa.Column('item_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item_type_id'], ['item_type.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_item_subtype_updated_at'), 'item_subtype', ['updated_at'], unique=False)
    op.add_column('item', sa.Column('item_subtype_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'item', 'item_subtype', ['item_subtype_id'], ['id'], ondelete='CASCADE')
    op.drop_column('item', 'price')
    op.drop_column('item', 'person')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('person', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('item', sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'item', type_='foreignkey')
    op.drop_column('item', 'item_subtype_id')
    op.drop_index(op.f('ix_item_subtype_updated_at'), table_name='item_subtype')
    op.drop_table('item_subtype')
    # ### end Alembic commands ###