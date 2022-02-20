"""Adding owner in company

Revision ID: e3a30dca0cd6
Revises: d332feeb5e7e
Create Date: 2022-02-15 20:34:45.078495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3a30dca0cd6'
down_revision = 'd332feeb5e7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_model')
    op.add_column('company', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'company', 'user', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'company', type_='foreignkey')
    op.drop_column('company', 'owner_id')
    op.create_table('user_model',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('is_staff', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_model_pkey'),
    sa.UniqueConstraint('email', name='user_model_email_key')
    )
    # ### end Alembic commands ###
