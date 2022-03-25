"""empty message

Revision ID: fe39e7e5d7c8
Revises: 4828516752f0
Create Date: 2022-03-25 07:57:48.777685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe39e7e5d7c8'
down_revision = '4828516752f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_stafff')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_stafff', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###