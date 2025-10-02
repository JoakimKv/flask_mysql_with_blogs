
# db_for_tests.py


import pymysql
import click
from flask import g
from flask.cli import with_appcontext

from flaskr_carved_rock.db_connection_wrapper import DBConnectionWrapper
from flaskr_carved_rock.database_connection_data import DatabaseConnectionData


def get_db(testing = True):

   """Connect to the application's configured MySQL test database."""

   databaseConnectionData = DatabaseConnectionData(testing = testing)

   username = databaseConnectionData.username
   password = databaseConnectionData.password
   database = databaseConnectionData.database
   host = databaseConnectionData.host
   port = databaseConnectionData.port
   sslDisabled = databaseConnectionData.sslDisabled

   if "db" not in g:

      conn = pymysql.connect(
         host = host,  # or Docker container name if using Docker Compose
         port = port,
         user = username,
         password = password,
         database = database,
         ssl = {"ssl": {}} if not sslDisabled else None,         
         cursorclass = pymysql.cursors.DictCursor  # rows behave like sqlite3.Row
      )
      g.db = DBConnectionWrapper(conn = conn, testing = testing)

   return g.db

def close_db(e = None):

   """Close the database at the end of the request or CLI command."""

   db = g.pop("db", None)
   if db is not None:
      
      try:
         
         db.close()

      except Exception:
         
         pass

def init_db():

   """Initialize the test database with schema.sql."""
   
   db = get_db()

   # Disable foreign key checks before dropping tables
   db.execute("SET FOREIGN_KEY_CHECKS = 0;")

   with open("tests/schema.sql", "r") as f:
      
      schema = f.read()

      for statement in schema.split(";"):
         
         if statement.strip():

            db.execute(statement)

   # Re-enable foreign key checks after recreation
   db.execute("SET FOREIGN_KEY_CHECKS = 1;")
   db.commit()


@click.command("init-db")
@with_appcontext
def init_db_command():

   """Clear existing data and create new tables."""

   init_db()
   click.echo("Initialized the test database.")


def init_app(app):

   """Register database functions with the Flask app (for tests)."""

   app.teardown_appcontext(close_db)
   app.cli.add_command(init_db_command)
