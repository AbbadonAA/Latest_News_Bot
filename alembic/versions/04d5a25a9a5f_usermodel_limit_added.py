"""UserModel limit added

Revision ID: 04d5a25a9a5f
Revises: 42ec8808acf7
Create Date: 2023-04-03 00:13:33.297383

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '04d5a25a9a5f'
down_revision = '42ec8808acf7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('article_limit', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'article_limit')
    # ### end Alembic commands ###
