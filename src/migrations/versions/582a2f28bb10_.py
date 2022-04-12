"""empty message

Revision ID: 582a2f28bb10
Revises: 84eb3eaa2bf1
Create Date: 2022-04-13 04:25:25.674847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '582a2f28bb10'
down_revision = '84eb3eaa2bf1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location_item_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('item_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_type_id'], ['item_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_location_item_type_updated_at'), 'location_item_type', ['updated_at'], unique=False)
    op.drop_constraint('day_picker_item_subtype_id_fkey', 'day_picker', type_='foreignkey')
    op.drop_column('day_picker', 'item_subtype_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('day_picker', sa.Column('item_subtype_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('day_picker_item_subtype_id_fkey', 'day_picker', 'item_subtype', ['item_subtype_id'], ['id'], ondelete='CASCADE')
    op.drop_index(op.f('ix_location_item_type_updated_at'), table_name='location_item_type')
    op.drop_table('location_item_type')
    # ### end Alembic commands ###
