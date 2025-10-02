"""step1

Revision ID: 814ad779229f
Revises: 786888a1190c
Create Date: 2025-09-14 13:18:20.648907

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '814ad779229f'
down_revision = '786888a1190c'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = inspect(conn)

    # --- Handle post table ---
    fks = [fk['name'] for fk in inspector.get_foreign_keys('post')]
    if 'fk_post_author' in fks:
        with op.batch_alter_table('post', schema=None) as batch_op:
            batch_op.drop_constraint('fk_post_author', type_='foreignkey')

    # --- Handle user table ---
    columns = [col['name'] for col in inspector.get_columns('user')]
    if 'uuid' not in columns:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.add_column(sa.Column('uuid', sa.String(length=64), nullable=False))


def downgrade():
    conn = op.get_bind()
    inspector = inspect(conn)

    # --- Handle user table ---
    columns = [col['name'] for col in inspector.get_columns('user')]
    if 'uuid' in columns:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.drop_column('uuid')

    # --- Handle post table ---
    fks = [fk['name'] for fk in inspector.get_foreign_keys('post')]
    if 'fk_post_author' not in fks:
        with op.batch_alter_table('post', schema=None) as batch_op:
            batch_op.create_foreign_key('fk_post_author', 'user', ['author_id'], ['id'])
