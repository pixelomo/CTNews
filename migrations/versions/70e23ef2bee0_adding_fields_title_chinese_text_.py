"""adding fields title_chinese, text_indonesian, title_indonesian

Revision ID: 70e23ef2bee0
Revises: da15d870f9a3
Create Date: 2023-06-09 10:07:36.434488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70e23ef2bee0'
down_revision = 'da15d870f9a3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('article', sa.Column('title_chinese', sa.String(length=1000), nullable=True))
    op.add_column('article', sa.Column('text_indonesian', sa.Text(), nullable=True))
    op.add_column('article', sa.Column('title_indonesian', sa.String(length=1000), nullable=True))

def downgrade():
    op.drop_column('article', 'title_chinese')
    op.drop_column('article', 'text_indonesian')
    op.drop_column('article', 'title_indonesian')
