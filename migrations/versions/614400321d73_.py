"""empty message

Revision ID: 614400321d73
Revises: d914567d90de
Create Date: 2022-03-21 09:09:11.233722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '614400321d73'
down_revision = 'd914567d90de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'company', 'user', ['owner_id'], ['id'], ondelete='CASCADE', use_alter=True)
    op.create_foreign_key(None, 'office', 'company', ['company_id'], ['id'], ondelete='CASCADE', use_alter=True)
    op.create_foreign_key(None, 'user', 'office', ['office_id'], ['id'], ondelete='SET NULL', use_alter=True)
    op.create_foreign_key(None, 'user', 'user', ['chief_id'], ['id'], ondelete='CASCADE', use_alter=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'office', type_='foreignkey')
    op.drop_constraint(None, 'company', type_='foreignkey')
    # ### end Alembic commands ###
