"""adding fields title_korean, text_korean

Revision ID: 7eff2f4132e2
Revises: 70e23ef2bee0
Create Date: 2023-06-22 12:48:42.160145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7eff2f4132e2'
down_revision = '70e23ef2bee0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('article', sa.Column('title_korean', sa.String(length=1000), nullable=True))
    op.add_column('article', sa.Column('text_korean', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('article', 'title_korean')
    op.drop_column('article', 'text_korean')
