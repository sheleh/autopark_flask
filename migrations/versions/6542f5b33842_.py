"""empty message

Revision ID: 6542f5b33842
Revises: 71b3ded4835c
Create Date: 2022-03-22 08:34:38.885141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6542f5b33842'
down_revision = '71b3ded4835c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_chief_id_fkey', 'user', type_='foreignkey')
    op.create_foreign_key(None, 'user', 'user', ['chief_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.create_foreign_key('user_chief_id_fkey', 'user', 'user', ['chief_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
