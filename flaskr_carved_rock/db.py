
# db.py


import pymysql
import click
from flask import current_app, g
from flask.cli import with_appcontext

from flaskr_carved_rock.db_connection_wrapper import DBConnectionWrapper
from flaskr_carved_rock.database_connection_data import DatabaseConnectionData


def get_db(testing = False):

   """Connect to the application's configured MySQL database."""
           
   databaseConnectionData = DatabaseConnectionData(testing = testing)

   username = databaseConnectionData.username
   password = databaseConnectionData.password
   host = databaseConnectionData.host
   port = databaseConnectionData.port
   sslDisabled = databaseConnectionData.sslDisabled


   if "db" not in g:

      conn = pymysql.connect(
         host = host,  # or Docker container name if using Docker Compose
         port = port,
         user = username,
         password = password,
         database = current_app.config["DATABASE"],  # set in Flask config
         ssl = {"ssl": {}} if not sslDisabled else None,
         cursorclass = pymysql.cursors.DictCursor  # rows behave like sqlite3.Row
      ) 
        
      g.db = DBConnectionWrapper(conn)

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

   """Run schema.sql on the MySQL database."""

   db = get_db()

   with current_app.open_resource("schema.sql") as f:
      
      sql = f.read().decode("utf8")

      for statement in sql.split(";"):  # MySQL needs individual statements.

        if statement.strip():

            db.execute(statement)

        db.commit()


@click.command("init-db")
@with_appcontext
def init_db_command():

   """Clear existing data and create new tables."""

   init_db()
   click.echo("Initialized the database.")

def init_app(app):

   """Register database functions with the Flask app."""

   app.teardown_appcontext(close_db)
   app.cli.add_command(init_db_command)
