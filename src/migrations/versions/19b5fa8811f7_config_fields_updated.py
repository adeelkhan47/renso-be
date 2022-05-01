"""config fields updated

Revision ID: 19b5fa8811f7
Revises: d2bcca5f1c72
Create Date: 2022-04-20 17:25:17.999843

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19b5fa8811f7'
down_revision = 'd2bcca5f1c72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('front_end_configs', sa.Column('email', sa.String(), nullable=True))
    op.add_column('front_end_configs', sa.Column('email_password', sa.String(), nullable=True))
    op.add_column('front_end_configs', sa.Column('privacy_policy_link', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('front_end_configs', 'privacy_policy_link')
    op.drop_column('front_end_configs', 'email_password')
    op.drop_column('front_end_configs', 'email')
    # ### end Alembic commands ###