"""followers

Revision ID: 83703d7c6d48
Revises: 5a4187673912
Create Date: 2021-03-06 14:35:14.886791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83703d7c6d48'
down_revision = '5a4187673912'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###