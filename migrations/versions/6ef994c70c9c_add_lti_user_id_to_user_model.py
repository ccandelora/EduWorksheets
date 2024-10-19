"""Add lti_user_id to User model

Revision ID: 6ef994c70c9c
Revises: c93a748999ff
Create Date: 2023-10-19 14:37:21.013456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ef994c70c9c'
down_revision = 'c93a748999ff'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash', type_=sa.String(255))
        batch_op.add_column(sa.Column('lti_user_id', sa.String(255), nullable=True))
        batch_op.create_unique_constraint(None, ['lti_user_id'])


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('lti_user_id')
        batch_op.alter_column('password_hash', type_=sa.String(128))
