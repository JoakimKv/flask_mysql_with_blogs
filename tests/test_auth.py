
# tests/test_auth.py

import pytest

# This assumes you already have the AuthActions fixture in conftest.py
# and the db_transaction fixture if you need DB access


def test_hello_route(client):

    """Simple test to check the /hello route works."""

    response = client.get("/hello")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data

def test_register_login_logout(auth):

    """Test logging in and logging out with the existing testuser."""

    # Login with the test user created in conftest.py
    response = auth.login(username="testuser", password="testpass")
    assert response.status_code == 200
    assert b"Log Out" in response.data  # typical post-login check

    # Logout
    response = auth.logout()
    assert response.status_code == 200
    assert b"Log In" in response.data  # confirm logged out


def test_invalid_login(auth):
    
    """Test login with invalid credentials."""

    response = auth.login(username="wronguser", password="wrongpass")
    assert response.status_code == 200
    # Either username or password error messages
    assert (b"Incorrect username" in response.data
            or b"Incorrect password" in response.data)
