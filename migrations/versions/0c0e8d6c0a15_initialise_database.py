"""Initialise database

Revision ID: 0c0e8d6c0a15
Revises: dff07c42ca91
Create Date: 2025-02-26 10:50:49.304434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c0e8d6c0a15'
down_revision = 'dff07c42ca91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('date_added', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_item', schema=None) as batch_op:
        batch_op.drop_column('date_added')
        batch_op.drop_column('image_url')

    # ### end Alembic commands ###
