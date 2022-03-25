"""empty message

Revision ID: 71b3ded4835c
Revises: 2aceeebda647
Create Date: 2022-03-22 08:31:12.959302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71b3ded4835c'
down_revision = '2aceeebda647'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_company_id_fkey', 'user', type_='foreignkey')
    op.drop_constraint('user_office_id_fkey', 'user', type_='foreignkey')
    op.create_foreign_key(None, 'user', 'office', ['office_id'], ['id'], ondelete='SET NULL', use_alter=True)
    op.create_foreign_key(None, 'user', 'company', ['company_id'], ['id'], ondelete='SET NULL', use_alter=True)
    op.drop_constraint('vehicle_office_id_fkey', 'vehicle', type_='foreignkey')
    op.drop_constraint('vehicle_company_id_fkey', 'vehicle', type_='foreignkey')
    op.create_foreign_key(None, 'vehicle', 'office', ['office_id'], ['id'], ondelete='SET NULL', use_alter=True)
    op.create_foreign_key(None, 'vehicle', 'company', ['company_id'], ['id'], ondelete='SET NULL', use_alter=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vehicle', type_='foreignkey')
    op.drop_constraint(None, 'vehicle', type_='foreignkey')
    op.create_foreign_key('vehicle_company_id_fkey', 'vehicle', 'company', ['company_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('vehicle_office_id_fkey', 'vehicle', 'office', ['office_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.create_foreign_key('user_office_id_fkey', 'user', 'office', ['office_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('user_company_id_fkey', 'user', 'company', ['company_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
