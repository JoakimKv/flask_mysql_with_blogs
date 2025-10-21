
#!/usr/bin/env sh

set -e

echo "[Entrypoint] Starting Flask app with Gunicorn..."

# If you have any pre-start tasks, you can add them here.
# Example: database migrations (Alembic) or copying demo data
# flask db upgrade || true

exec gunicorn -w 4 -b 0.0.0.0:5000 flaskr_carved_rock:create_app
