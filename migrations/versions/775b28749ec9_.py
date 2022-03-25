"""empty message

Revision ID: 775b28749ec9
Revises: 676f43192506
Create Date: 2022-03-23 17:42:26.108318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '775b28749ec9'
down_revision = '676f43192506'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('company_owner_id_key', 'company', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('company_owner_id_key', 'company', ['owner_id'])
    # ### end Alembic commands ###