"""add text_chinese field

Revision ID: da15d870f9a3
Revises: a2341978634
Create Date: 2023-06-07 12:14:39.276911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da15d870f9a3'
down_revision = 'a2341978634'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('article', sa.Column('text_chinese', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('article', 'text_chinese')

