"""empty message

Revision ID: e614e84a43dd
Revises: 041651b617fc
Create Date: 2022-04-10 21:05:22.903587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e614e84a43dd'
down_revision = '041651b617fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('associate_email', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_associate_email_user_id'), 'associate_email', ['user_id'], unique=False)
    op.create_foreign_key(None, 'associate_email', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('booking', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_booking_user_id'), 'booking', ['user_id'], unique=False)
    op.create_foreign_key(None, 'booking', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('booking_widget', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_booking_widget_user_id'), 'booking_widget', ['user_id'], unique=False)
    op.create_foreign_key(None, 'booking_widget', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('custom_parameter', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_custom_parameter_user_id'), 'custom_parameter', ['user_id'], unique=False)
    op.create_foreign_key(None, 'custom_parameter', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('item', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_item_user_id'), 'item', ['user_id'], unique=False)
    op.create_foreign_key(None, 'item', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('item_subtype', sa.Column('user_key', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_item_subtype_user_key'), 'item_subtype', ['user_key'], unique=False)
    op.create_foreign_key(None, 'item_subtype', 'user', ['user_key'], ['id'], ondelete='CASCADE')
    op.add_column('item_type', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_item_type_user_id'), 'item_type', ['user_id'], unique=False)
    op.create_foreign_key(None, 'item_type', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('language', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_language_user_id'), 'language', ['user_id'], unique=False)
    op.create_foreign_key(None, 'language', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('location', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_location_user_id'), 'location', ['user_id'], unique=False)
    op.create_foreign_key(None, 'location', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('order', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_order_user_id'), 'order', ['user_id'], unique=False)
    op.create_foreign_key(None, 'order', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('payment_method', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_payment_method_user_id'), 'payment_method', ['user_id'], unique=False)
    op.create_foreign_key(None, 'payment_method', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('season', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_season_user_id'), 'season', ['user_id'], unique=False)
    op.create_foreign_key(None, 'season', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('tag', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_tag_user_id'), 'tag', ['user_id'], unique=False)
    op.create_foreign_key(None, 'tag', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('tax', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_tax_user_id'), 'tax', ['user_id'], unique=False)
    op.create_foreign_key(None, 'tax', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('user', sa.Column('user_key', sa.String(), nullable=False))
    op.create_index(op.f('ix_user_user_key'), 'user', ['user_key'], unique=True)
    op.add_column('voucher', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_voucher_user_id'), 'voucher', ['user_id'], unique=False)
    op.create_foreign_key(None, 'voucher', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'voucher', type_='foreignkey')
    op.drop_index(op.f('ix_voucher_user_id'), table_name='voucher')
    op.drop_column('voucher', 'user_id')
    op.drop_index(op.f('ix_user_user_key'), table_name='user')
    op.drop_column('user', 'user_key')
    op.drop_constraint(None, 'tax', type_='foreignkey')
    op.drop_index(op.f('ix_tax_user_id'), table_name='tax')
    op.drop_column('tax', 'user_id')
    op.drop_constraint(None, 'tag', type_='foreignkey')
    op.drop_index(op.f('ix_tag_user_id'), table_name='tag')
    op.drop_column('tag', 'user_id')
    op.drop_constraint(None, 'season', type_='foreignkey')
    op.drop_index(op.f('ix_season_user_id'), table_name='season')
    op.drop_column('season', 'user_id')
    op.drop_constraint(None, 'payment_method', type_='foreignkey')
    op.drop_index(op.f('ix_payment_method_user_id'), table_name='payment_method')
    op.drop_column('payment_method', 'user_id')
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_index(op.f('ix_order_user_id'), table_name='order')
    op.drop_column('order', 'user_id')
    op.drop_constraint(None, 'location', type_='foreignkey')
    op.drop_index(op.f('ix_location_user_id'), table_name='location')
    op.drop_column('location', 'user_id')
    op.drop_constraint(None, 'language', type_='foreignkey')
    op.drop_index(op.f('ix_language_user_id'), table_name='language')
    op.drop_column('language', 'user_id')
    op.drop_constraint(None, 'item_type', type_='foreignkey')
    op.drop_index(op.f('ix_item_type_user_id'), table_name='item_type')
    op.drop_column('item_type', 'user_id')
    op.drop_constraint(None, 'item_subtype', type_='foreignkey')
    op.drop_index(op.f('ix_item_subtype_user_key'), table_name='item_subtype')
    op.drop_column('item_subtype', 'user_key')
    op.drop_constraint(None, 'item', type_='foreignkey')
    op.drop_index(op.f('ix_item_user_id'), table_name='item')
    op.drop_column('item', 'user_id')
    op.drop_constraint(None, 'custom_parameter', type_='foreignkey')
    op.drop_index(op.f('ix_custom_parameter_user_id'), table_name='custom_parameter')
    op.drop_column('custom_parameter', 'user_id')
    op.drop_constraint(None, 'booking_widget', type_='foreignkey')
    op.drop_index(op.f('ix_booking_widget_user_id'), table_name='booking_widget')
    op.drop_column('booking_widget', 'user_id')
    op.drop_constraint(None, 'booking', type_='foreignkey')
    op.drop_index(op.f('ix_booking_user_id'), table_name='booking')
    op.drop_column('booking', 'user_id')
    op.drop_constraint(None, 'associate_email', type_='foreignkey')
    op.drop_index(op.f('ix_associate_email_user_id'), table_name='associate_email')
    op.drop_column('associate_email', 'user_id')
    # ### end Alembic commands ###
