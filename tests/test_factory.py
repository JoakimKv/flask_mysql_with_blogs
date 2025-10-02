
# tests/test_factory.py


import pytest
from flaskr_carved_rock import create_app


# ------------------------------
# Fixtures
# ------------------------------

@pytest.fixture
def app_no_db():

    """
    Create a minimal app instance for tests that don't need DB access.
    This avoids triggering db_transaction fixture.
    """
    return create_app(testing = True)


@pytest.fixture
def client_no_db(app_no_db):

    """A test client for the minimal app."""
    return app_no_db.test_client()


# ------------------------------
# Tests
# ------------------------------

def test_config(app_no_db):

    """Test create_app without passing test config."""

    app_default = create_app()
    assert not app_default.testing

    app_test = create_app(testing = True)
    assert app_test.testing


def test_hello(client_no_db):
    
    """Test the /hello route returns the expected string."""
    
    response = client_no_db.get("/hello")
    assert response.get_data(as_text=True) == "Hello, World!"
