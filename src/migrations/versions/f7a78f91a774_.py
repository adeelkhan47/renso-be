"""empty message

Revision ID: f7a78f91a774
Revises: 9e45384ec7c7
Create Date: 2022-05-31 00:08:31.924930

"""

# revision identifiers, used by Alembic.
from alembic import op
from sqlalchemy import MetaData, Table

revision = 'f7a78f91a774'
down_revision = '9e45384ec7c7'
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind())

    meta.reflect(only=("order_status",))

    item_status = Table("order_status", meta)
    op.bulk_insert(
        item_status,
        [
            {
                "name": "Updated",
                "color": "orange",
            }])


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
