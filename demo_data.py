
# run this at the beginning of the course

from pathlib import Path
from flask import current_app
from flaskr_carved_rock import create_app
from flaskr_carved_rock.db import get_db, init_db

app = create_app()
app.app_context().push()
init_db()
db = get_db()
cursor = db.cursor()

with Path("demo_data.sql").open() as f:
    sql_commands = f.read().split(";")
    for command in sql_commands:
        command = command.strip()
        if command:  # skip empty commands
            cursor.execute(command)

db.commit()
cursor.close()
