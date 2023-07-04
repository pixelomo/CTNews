"""adding field title

Revision ID: 5f71f381852b
Revises: 9d3c62bf80a4
Create Date: 2023-07-04 11:57:34.681833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f71f381852b'
down_revision = '9d3c62bf80a4'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("article_stats", sa.Column("title", sa.String(), nullable=True))

def downgrade():
    op.drop_column("article_stats", "title")
