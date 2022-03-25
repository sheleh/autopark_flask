"""empty message

Revision ID: 633b7bfc35e0
Revises: b49d7585f181
Create Date: 2022-03-21 08:33:25.867863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '633b7bfc35e0'
down_revision = 'b49d7585f181'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE', use_alter=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('owner_id')
    )
    op.create_table('office',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='CASCADE', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('revoked_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('is_stafff', sa.Boolean(), nullable=True),
    sa.Column('chief_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('office_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chief_id'], ['user.id'], ondelete='CASCADE', use_alter=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['office_id'], ['office.id'], ondelete='SET NULL', use_alter=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('vehicle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('license_plate', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('model', sa.String(), nullable=True),
    sa.Column('year_of_manufacture', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('office_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['office_id'], ['office.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('drivers_association',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicle.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'vehicle_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('drivers_association')
    op.drop_table('vehicle')
    op.drop_table('user')
    op.drop_table('revoked_tokens')
    op.drop_table('office')
    op.drop_table('company')
    # ### end Alembic commands ###
