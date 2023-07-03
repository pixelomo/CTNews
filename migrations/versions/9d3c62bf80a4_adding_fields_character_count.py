"""adding fields character_count

Revision ID: 9d3c62bf80a4
Revises: 7eff2f4132e2
Create Date: 2023-07-03 13:09:57.557315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d3c62bf80a4'
down_revision = '7eff2f4132e2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('article_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pubDate', sa.DateTime(), nullable=False),
    sa.Column('source', sa.String(length=200), nullable=False),
    sa.Column('character_count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('article_stats')
