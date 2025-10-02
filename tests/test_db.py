
# tests/test_db.py


import pytest
import pymysql
from flask import g
from flaskr_carved_rock import create_app
from tests.db_for_tests import get_db, close_db

from flaskr_carved_rock.database_connection_data import DatabaseConnectionData


# ------------------------------
# Fixtures
# ------------------------------

@pytest.fixture
def app(testing = True):

   """Create and configure a new app instance for testing."""

   app = create_app(testing = testing)
   yield app

@pytest.fixture
def client(app):

   """A test client for the app."""

   return app.test_client()

@pytest.fixture
def runner(app):

   """A test runner for CLI commands."""

   return app.test_cli_runner()

@pytest.fixture
def db_transaction(app):

   """
   Provide a DB connection wrapped in a transaction that rolls back after test.
   Ensures tests never modify database permanently.
   """

   with app.app_context():
        
      connection = get_db()

      try:
            
            connection.autocommit = False  # start transaction.

      except pymysql.err.InterfaceError:
            
         # Connection may already be closed; ignore
         pass
      
      try:
         
         yield connection

      finally:
            
         # Rollback changes safely
         try:
                
            connection.rollback()

         except pymysql.err.InterfaceError:
                
            pass
         
         # Reset autocommit safely
         try:
                
            connection.autocommit = True

         except pymysql.err.InterfaceError:
                
            pass


# ------------------------------
# Tests
# ------------------------------

def test_get_close_db(db_transaction, app):

    with app.app_context():

        first_conn = get_db()
        second_conn = get_db()
        assert first_conn is second_conn

        close_db()

    with app.app_context():

        assert "db" not in g

    # Old connection should be unusable
    with pytest.raises((pymysql.err.ProgrammingError, pymysql.err.InterfaceError)):
        
        db_transaction.close()
        db_transaction.execute("SELECT 1")

def test_simple_query(db_transaction, testing = True):

   """Verify we can query the MySQL test database."""

   databaseConnectionData = DatabaseConnectionData(testing = testing)
   database = databaseConnectionData.database

   with db_transaction.cursor() as cursor:
      
      cursor.execute("SELECT DATABASE() AS db_name")
      result = cursor.fetchone()
      assert result["db_name"] == database

   with db_transaction.cursor() as cursor:
        
      cursor.execute("SELECT 1 AS test_value")
      result = cursor.fetchone()
      assert result["test_value"] == 1

def test_init_db_command(runner, monkeypatch):

   """Test the init-db CLI command without touching production DB."""

   class Recorder:
      
      called = False

   def fake_init_db():
        
      # Only record that init_db would be called
      Recorder.called = True

   # Replace real init_db with fake function
   monkeypatch.setattr("flaskr_carved_rock.db.init_db", fake_init_db)
   result = runner.invoke(args=["init-db"])

   assert "Initialized" in result.output
   assert Recorder.called
