"""empty message

Revision ID: 1a60179af3c4
Revises: 78699db88305
Create Date: 2022-02-16 18:01:56.518717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a60179af3c4'
down_revision = '78699db88305'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('company_address_key', 'company', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('company_address_key', 'company', ['address'])
    # ### end Alembic commands ###
