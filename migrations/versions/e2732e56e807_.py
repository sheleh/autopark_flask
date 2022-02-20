"""empty message

Revision ID: e2732e56e807
Revises: 4935d83a30d9
Create Date: 2022-02-16 17:46:23.869299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2732e56e807'
down_revision = '4935d83a30d9'
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