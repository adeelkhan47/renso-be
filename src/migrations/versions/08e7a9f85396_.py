"""empty message

Revision ID: 08e7a9f85396
Revises: 6a45f353728c
Create Date: 2022-04-18 20:59:13.822699

"""
from alembic import op
from sqlalchemy import MetaData, Table

# revision identifiers, used by Alembic.
revision = '08e7a9f85396'
down_revision = '6a45f353728c'
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind())

    meta.reflect(only=("booking_status",))

    item_status = Table("booking_status", meta)
    op.bulk_insert(
        item_status,
        [
            {
                "name": "Pending",
                "color": "orange",
            }
        ],
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
