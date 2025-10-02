
# tests/test_change_password.py


import pytest
from flaskr_carved_rock.models import User
from flaskr_carved_rock.sqla import sqla


@pytest.fixture
def password_user(app):
    
    """Create a test user 'pwd_tester' for password change tests."""

    with app.app_context():
        
        # Cleanup any old test user
        sqla.session.query(User).filter_by(username="pwd_tester").delete()
        sqla.session.commit()

        # Create a new user
        user = User(username="pwd_tester", password="oldpass234")
        sqla.session.add(user)
        sqla.session.commit()

        yield user

        # Cleanup afterwards
        sqla.session.query(User).filter_by(username="pwd_tester").delete()
        sqla.session.commit()


def test_change_password(auth, client, app, password_user):
    
    """A logged-in user can change their password and log in with the new one."""

    # Log in with old password
    auth.login(username="pwd_tester", password="oldpass234")

    # Change password
    response = client.post(
        "/auth/change_password",
        data={
            "current_password": "oldpass234",
            "new_password": "newpass456",
            "confirm_password": "newpass456",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Password updated successfully." in response.data

    # Verify in DB: password is hashed and updated
    with app.app_context():
        user = sqla.session.query(User).filter_by(username="pwd_tester").first()
        assert user is not None
        assert user.correct_password("newpass456")
        assert not user.correct_password("oldpass234")

    # Log out
    client.get("/auth/logout", follow_redirects=True)

    # Verify login works with new password, not old
    login_resp = client.post(
        "/auth/login",
        data={"username": "pwd_tester", "password": "newpass456"},
        follow_redirects=True,
    )
    assert b"Log Out" in login_resp.data


def test_change_password_wrong_current(auth, client, app, password_user):
    
    """Password change fails if current password is incorrect."""

    auth.login(username="pwd_tester", password="oldpass234")

    response = client.post(
        "/auth/change_password",
        data={
            "current_password": "wrongpass",
            "new_password": "newpass456",
            "confirm_password": "newpass456",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Current password is incorrect." in response.data

    # Verify DB password is unchanged
    with app.app_context():
        
        user = sqla.session.query(User).filter_by(username="pwd_tester").first()
        assert user.correct_password("oldpass234")


def test_change_password_mismatch(auth, client, app, password_user):
    
    """Password change fails if new passwords do not match."""

    auth.login(username="pwd_tester", password="oldpass234")

    response = client.post(
        "/auth/change_password",
        data={
            "current_password": "oldpass234",
            "new_password": "newpass456",
            "confirm_password": "wrongconfirm",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"New passwords do not match." in response.data

    # Verify DB password is unchanged
    with app.app_context():
        
        user = sqla.session.query(User).filter_by(username="pwd_tester").first()
        assert user.correct_password("oldpass234")


def test_change_then_delete_account(auth, client, app, password_user):
    
    """A user can change their password, then delete their account."""

    # Log in with old password
    auth.login(username="pwd_tester", password="oldpass234")

    # Change password
    client.post(
        "/auth/change_password",
        data={
            "current_password": "oldpass234",
            "new_password": "newpass456",
            "confirm_password": "newpass456",
        },
        follow_redirects=True,
    )

    # Delete account
    response = client.post("/auth/delete_account", follow_redirects=True)
    assert response.status_code == 200
    assert b"Your account has been deleted permanently." in response.data

    # Verify user is gone from DB
    with app.app_context():
        
        user = sqla.session.query(User).filter_by(username="pwd_tester").first()
        assert user is None
