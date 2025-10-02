
"""step2

Revision ID: 6392fde05718
Revises: 814ad779229f
Create Date: 2025-09-14 13:48:41.118559

"""

# revision identifiers, used by Alembic.
revision = '6392fde05718'
down_revision = '814ad779229f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


def upgrade():
    
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('user')]

    with op.batch_alter_table('user', schema=None) as batch_op:
        # Add api_key only if it doesn't exist
        if 'api_key' not in columns:
            batch_op.add_column(sa.Column('api_key', sa.String(64), nullable=True))

        # Make sure username is VARCHAR(150) and not TEXT
        batch_op.alter_column(
            'username',
            existing_type=sa.Text(),
            type_=sa.String(150),
            existing_nullable=False,
            nullable=False
        )

        # Recreate unique constraint on username (if needed)
        batch_op.create_unique_constraint('uq_user_username', ['username'])


def downgrade():
    
    with op.batch_alter_table('user', schema=None) as batch_op:
        # Drop api_key column if it exists
        batch_op.drop_column('api_key')
