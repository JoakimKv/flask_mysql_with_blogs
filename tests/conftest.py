
# conftest.py


import os
import pytest
from uuid import uuid4
from sqlalchemy.orm import sessionmaker
from flask.testing import FlaskClient
from flaskr_carved_rock import create_app
from flaskr_carved_rock.sqla import sqla
from flaskr_carved_rock.models import User

from flaskr_carved_rock.database_connection_data import DatabaseConnectionData


# -----------------------------
# Fixtures
# -----------------------------

@pytest.fixture
def app(testing = True):

    """Create a Flask app configured for testing."""
    
    databaseConnectionData = DatabaseConnectionData(testing = testing)

    username = databaseConnectionData.username
    password = databaseConnectionData.password
    port = databaseConnectionData.port
    host = databaseConnectionData.host
    sslDisabled = databaseConnectionData.sslDisabled
    database = databaseConnectionData.database

    sslParam = "ssl=true" if not sslDisabled else "ssl_disabled=true"

    app = create_app(testing = testing)

    # Override template/static folders if needed
    template_path = os.path.join(os.path.dirname(__file__), "../flaskr_carved_rock/templates")
    static_path = os.path.join(os.path.dirname(__file__), "../flaskr_carved_rock/static")
    app.template_folder = template_path
    app.static_folder = static_path

    app.config.update({
        "SQLALCHEMY_DATABASE_URI": os.getenv(
            "SQLALCHEMY_TEST_DATABASE_URI",
            f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?{sslParam}"
        ),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "TESTING": testing,
         "WTF_CSRF_ENABLED": False  # disable CSRF for tests
    })

    with app.app_context():

        # Create tables if missing
        sqla.create_all()

        # Remove test users if they exist
        sqla.session.query(User).filter(User.username.in_(["testuser", "otheruser"])).delete()
        sqla.session.commit()

        # Recreate test users with UUIDs
        test_user = User(
            username="testuser",
            password="testpass",
            uuid=str(uuid4())
        )

        other_user = User(
            username="otheruser",
            password="otherpass",
            uuid=str(uuid4())
        )

        sqla.session.add_all([test_user, other_user])
        sqla.session.commit()

    yield app

    with app.app_context():
        sqla.session.remove()

@pytest.fixture
def client(app) -> FlaskClient:

    """Flask test client."""

    return app.test_client()


@pytest.fixture
def runner(app):

    """CLI runner for Flask."""

    return app.test_cli_runner()


@pytest.fixture
def db_transaction(app):

    """Provide a SQLAlchemy session wrapped in a transaction for each test."""

    with app.app_context():

        connection = sqla.engine.connect()
        transaction = connection.begin()
        Session = sessionmaker(bind=connection)
        session = Session()

        try:

            # Yield session for test; do NOT recreate users here
            yield session

        finally:

            session.rollback()
            transaction.rollback()
            connection.close()
            session.close()


# -----------------------------
# Auth helper
# -----------------------------

class AuthActions:

    """Helper to log in/out a test client user."""

    def __init__(self, client: FlaskClient):

        self._client = client

    def login(self, username="testuser", password="testpass"):

        """Log in with default test credentials."""

        return self._client.post(
            "/auth/login",
            data={"username": username, "password": password},
            follow_redirects=True
        )

    def logout(self):

        """Log out the current test user."""

        return self._client.get("/auth/logout", follow_redirects=True)


# -----------------------------
# Auth fixture
# -----------------------------

@pytest.fixture
def auth(client):

    """Return an authenticated test client helper."""

    return AuthActions(client)
