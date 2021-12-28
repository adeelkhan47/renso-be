"""empty message

Revision ID: 55fa4a4af763
Revises: 
Create Date: 2021-12-23 23:11:18.427482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55fa4a4af763'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booking_widget',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('date_Picker', sa.Boolean(), nullable=False),
    sa.Column('time_Picker', sa.Boolean(), nullable=False),
    sa.Column('date_range_Picker', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date_Picker'),
    sa.UniqueConstraint('date_range_Picker'),
    sa.UniqueConstraint('time_Picker')
    )
    op.create_index(op.f('ix_booking_widget_updated_at'), 'booking_widget', ['updated_at'], unique=False)
    op.create_table('item_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('maintenance', sa.Integer(), nullable=False),
    sa.Column('delivery_available', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('maintenance')
    )
    op.create_index(op.f('ix_item_type_updated_at'), 'item_type', ['updated_at'], unique=False)
    op.create_table('language',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_language_updated_at'), 'language', ['updated_at'], unique=False)
    op.create_table('order',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('client_name', sa.String(), nullable=False),
    sa.Column('client_email', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('time_period', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_updated_at'), 'order', ['updated_at'], unique=False)
    op.create_table('payment_method',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_payment_method_updated_at'), 'payment_method', ['updated_at'], unique=False)
    op.create_table('tax',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('percentage', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_tax_updated_at'), 'tax', ['updated_at'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('subscription', sa.String(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_updated_at'), 'user', ['updated_at'], unique=False)
    op.create_table('day_picker',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('monday', sa.Boolean(), nullable=False),
    sa.Column('tuesday', sa.Boolean(), nullable=False),
    sa.Column('wednesday', sa.Boolean(), nullable=False),
    sa.Column('thursday', sa.Boolean(), nullable=False),
    sa.Column('friday', sa.Boolean(), nullable=False),
    sa.Column('saturday', sa.Boolean(), nullable=False),
    sa.Column('sunday', sa.Boolean(), nullable=False),
    sa.Column('item_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_type_id'], ['item_type.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('item_type_id')
    )
    op.create_index(op.f('ix_day_picker_updated_at'), 'day_picker', ['updated_at'], unique=False)
    op.create_table('item',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('tags', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('item_type_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_type_id'], ['item_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_updated_at'), 'item', ['updated_at'], unique=False)
    op.create_table('payment_tax',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('tax_id', sa.Integer(), nullable=False),
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['payment_id'], ['payment_method.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tax_id'], ['tax.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payment_tax_updated_at'), 'payment_tax', ['updated_at'], unique=False)
    op.create_table('booking',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('discount', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('start_time', sa.String(), nullable=False),
    sa.Column('end_time', sa.String(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_booking_updated_at'), 'booking', ['updated_at'], unique=False)
    op.create_table('time_picker',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('day', sa.String(), nullable=False),
    sa.Column('day_picker_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['day_picker_id'], ['day_picker.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_time_picker_updated_at'), 'time_picker', ['updated_at'], unique=False)
    op.create_table('order_bookings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_bookings_updated_at'), 'order_bookings', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_bookings_updated_at'), table_name='order_bookings')
    op.drop_table('order_bookings')
    op.drop_index(op.f('ix_time_picker_updated_at'), table_name='time_picker')
    op.drop_table('time_picker')
    op.drop_index(op.f('ix_booking_updated_at'), table_name='booking')
    op.drop_table('booking')
    op.drop_index(op.f('ix_payment_tax_updated_at'), table_name='payment_tax')
    op.drop_table('payment_tax')
    op.drop_index(op.f('ix_item_updated_at'), table_name='item')
    op.drop_table('item')
    op.drop_index(op.f('ix_day_picker_updated_at'), table_name='day_picker')
    op.drop_table('day_picker')
    op.drop_index(op.f('ix_user_updated_at'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_tax_updated_at'), table_name='tax')
    op.drop_table('tax')
    op.drop_index(op.f('ix_payment_method_updated_at'), table_name='payment_method')
    op.drop_table('payment_method')
    op.drop_index(op.f('ix_order_updated_at'), table_name='order')
    op.drop_table('order')
    op.drop_index(op.f('ix_language_updated_at'), table_name='language')
    op.drop_table('language')
    op.drop_index(op.f('ix_item_type_updated_at'), table_name='item_type')
    op.drop_table('item_type')
    op.drop_index(op.f('ix_booking_widget_updated_at'), table_name='booking_widget')
    op.drop_table('booking_widget')
    # ### end Alembic commands ###