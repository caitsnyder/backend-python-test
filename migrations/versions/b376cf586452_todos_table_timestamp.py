"""todos table timestamp

Revision ID: b376cf586452
Revises: be86aff211f2
Create Date: 2019-09-27 23:25:18.549004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b376cf586452'
down_revision = 'be86aff211f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todo', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_todo_timestamp'), 'todo', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_todo_timestamp'), table_name='todo')
    op.drop_column('todo', 'timestamp')
    # ### end Alembic commands ###
