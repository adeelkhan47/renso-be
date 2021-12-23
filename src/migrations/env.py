# region Model Imports
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.append("..")

import os

from model.base import Base
from model.user import User
from model.item import Item
from model.item_type import ItemType
from model.order_bookings import OrderBookings
from model.order import Order
from model.booking import Booking
from model.booking_widget import BookingWidget
from model.payment_method import PaymentMethod
from model.tax import Tax
from model.payment_tax import PaymentTax
from model.day_picker import DayPicker
from model.time_picker import TimePicker
from model.language import Language

config = context.config
config.set_main_option("sqlalchemy.url", "postgresql://postgres:postgres@localhost:5432/renso")
fileConfig(config.config_file_name, disable_existing_loggers=False)

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
