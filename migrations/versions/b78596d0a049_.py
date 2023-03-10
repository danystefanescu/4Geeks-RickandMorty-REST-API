"""empty message

Revision ID: b78596d0a049
Revises: e7f6502f373d
Create Date: 2023-01-21 19:01:51.970562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b78596d0a049'
down_revision = 'e7f6502f373d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=25), nullable=False))
        batch_op.create_unique_constraint(None, ['password'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('password')

    # ### end Alembic commands ###
