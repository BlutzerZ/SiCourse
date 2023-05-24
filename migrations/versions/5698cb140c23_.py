"""empty message

Revision ID: 5698cb140c23
Revises: 3d249966cce0
Create Date: 2023-05-24 20:53:33.923176

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5698cb140c23'
down_revision = '3d249966cce0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('thumbnail', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('createdAt', sa.Integer(), nullable=True))
        batch_op.alter_column('content',
               existing_type=mysql.VARCHAR(length=1000),
               type_=sa.String(length=2000),
               existing_nullable=False)

    with op.batch_alter_table('enrollment', schema=None) as batch_op:
        batch_op.drop_column('file_path')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('enrollment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_path', mysql.VARCHAR(length=200), nullable=True))

    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=sa.String(length=2000),
               type_=mysql.VARCHAR(length=1000),
               existing_nullable=False)
        batch_op.drop_column('createdAt')
        batch_op.drop_column('thumbnail')

    # ### end Alembic commands ###