"""empty message

Revision ID: f237b5060267
Revises: 0d3496a83f7f
Create Date: 2022-06-27 16:33:17.213752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f237b5060267'
down_revision = '0d3496a83f7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('street', sa.String(), nullable=True),
    sa.Column('street_number', sa.String(), nullable=True),
    sa.Column('zipcode', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('commercial_registered_number', sa.String(), nullable=True),
    sa.Column('legal_representative', sa.String(), nullable=True),
    sa.Column('email_for_taxs', sa.String(), nullable=True),
    sa.Column('company_tax_number', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_company_updated_at'), 'company', ['updated_at'], unique=False)
    op.create_index(op.f('ix_company_user_id'), 'company', ['user_id'], unique=False)
    op.add_column('item_subtype', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'item_subtype', 'company', ['company_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'item_subtype', type_='foreignkey')
    op.drop_column('item_subtype', 'company_id')
    op.drop_index(op.f('ix_company_user_id'), table_name='company')
    op.drop_index(op.f('ix_company_updated_at'), table_name='company')
    op.drop_table('company')
    # ### end Alembic commands ###
