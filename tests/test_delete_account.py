
# test_delete_account.py

# tests/test_delete_account.py

import pytest
from flaskr_carved_rock.models import User, Post
from flaskr_carved_rock.sqla import sqla

@pytest.fixture
def test_user_with_posts(app):
    
    """Create a test user 'kalle_test' with one post."""

    with app.app_context():
        
        # Clean up any previous test user
        sqla.session.query(User).filter_by(username="kalle_test").delete()
        sqla.session.commit()

        # Create user
        user = User(username="kalle_test", password="pass1")
        sqla.session.add(user)
        sqla.session.commit()

        # Create a post for cascade delete test
        post = Post(title="Test post", body="This is a test post", author_id=user.id)
        sqla.session.add(post)
        sqla.session.commit()

        yield user  # Provide the user for tests

        # Cleanup
        sqla.session.query(Post).filter_by(author_id=user.id).delete()
        sqla.session.query(User).filter_by(username="kalle_test").delete()
        sqla.session.commit()

def test_delete_own_account(auth, client, app):
    
    """A logged-in user can delete their own account."""
    
    # Log in as testuser
    auth.login(username="testuser", password="testpass")

    # Send POST to delete_account
    response = client.post("/auth/delete_account", follow_redirects=True)
    assert response.status_code == 200
    assert b"Your account has been deleted permanently." in response.data

    # Verify user is gone from DB
    with app.app_context():
        
        user = sqla.session.query(User).filter_by(username="testuser").first()
        assert user is None


def test_cannot_delete_other_user_account(auth, client, app):
    
    """A logged-in user cannot delete another user's account."""

    # Log in as testuser
    auth.login(username="testuser", password="testpass")

    # Use app context to access the DB
    with app.app_context():
        
        other_user = sqla.session.query(User).filter_by(username="otheruser").first()
        assert other_user is not None

    # Attempt to delete current user (the route always deletes current_user)
    response = client.post("/auth/delete_account", follow_redirects=True)
    assert response.status_code == 200

    # The flash message should indicate deletion of the current user, not other_user
    assert b"Your account has been deleted permanently." in response.data

    # Verify other_user still exists
    with app.app_context():
        
        user = sqla.session.query(User).filter_by(username="otheruser").first()
        assert user is not None
