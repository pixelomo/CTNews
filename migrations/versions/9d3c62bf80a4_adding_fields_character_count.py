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
    op.add_column('article', sa.Integer('character_count'), nullable=True),

def downgrade():
    op.drop_column('article', 'character_count')
