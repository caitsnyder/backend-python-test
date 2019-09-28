"""users table

Revision ID: 07a205657c19
Revises: 
Create Date: 2019-09-27 21:31:02.634270

"""
from alembic import op
import sqlalchemy as sa
# Use for seed
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date


# revision identifiers, used by Alembic.
revision = '07a205657c19'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('user') # For testing
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


    # Create an ad-hoc table for the seed
    user_table = table('user',
        column('id', Integer),
        column('username', String),
        column('password', String)
    )

    op.bulk_insert(user_table,
        [
            {'username':'user1', 'password':'user1'},
            {'username':'user2', 'password':'user2'},
            {'username':'user3', 'password':'user3'}
        ]
    )



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
