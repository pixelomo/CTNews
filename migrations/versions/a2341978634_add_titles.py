from alembic import op
import sqlalchemy as sa

revision = "a2341978634"
down_revision = "00e57c2afe7b"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("article", sa.Column("title_translated", sa.String(), nullable=True))

def downgrade():
    op.drop_column("article", "title_translated")
