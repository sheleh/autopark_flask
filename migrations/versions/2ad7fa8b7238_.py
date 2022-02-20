"""empty message

Revision ID: 2ad7fa8b7238
Revises: e1427b19deec
Create Date: 2022-02-16 15:33:30.520009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ad7fa8b7238'
down_revision = 'e1427b19deec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('role')
    op.drop_table('users_roles')
    op.drop_table('roles_parents')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles_parents',
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('parent_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['role.id'], name='roles_parents_parent_id_fkey'),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name='roles_parents_role_id_fkey')
    )
    op.create_table('users_roles',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name='users_roles_role_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='users_roles_user_id_fkey')
    )
    op.create_table('role',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='role_pkey')
    )
    # ### end Alembic commands ###