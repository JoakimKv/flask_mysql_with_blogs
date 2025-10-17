
# tests/test_blog.py


import pytest
from urllib.parse import unquote
from flaskr_carved_rock.models import User, Post
from flaskr_carved_rock.sqla import sqla


# -------------------------------------------------------------------
# Fixtures for posts
# -------------------------------------------------------------------

@pytest.fixture
def test_post(app):

    """Create a post for testing, removing any existing ones with the same title."""

    with app.app_context():

        # Delete existing test posts
        sqla.session.query(Post).filter_by(title="test title").delete()
        sqla.session.commit()

        test_user = sqla.session.query(User).filter_by(username="testuser").first()
        if not test_user:
            raise ValueError("Test user must exist (created in conftest.py)")

        post = Post(title="test title", body="test body", author_id=test_user.id)
        sqla.session.add(post)
        sqla.session.commit()

        return post.id


# -------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------

def test_index(client, auth, test_post):

    """Index page shows posts when logged in."""

    auth.login()
    response = client.get("/blogs/")
    assert response.status_code == 200
    assert b"Log Out" in response.data
    assert b"test title" in response.data

@pytest.mark.parametrize("path,next_url", [
    ("/blogs/create", "/blogs/create"),
    ("/blogs/1/update", "/blogs/1/update"),
    ("/blogs/1/delete", "/blogs/1/delete")
])
def test_login_required(client, path, next_url):

    """Non-logged-in users are redirected to login."""

    response = client.post(path, follow_redirects=False)
    assert response.status_code == 302
    location = unquote(response.headers["Location"])
    assert location.startswith("/blogs/")
    assert location.endswith(f"/login?next={next_url}")

def test_author_required(client, auth, app, test_post):

    """Only the post author can update/delete."""

    auth.login()
    with app.app_context():
        other_user = sqla.session.query(User).filter_by(username="otheruser").first()
        if not other_user:
            raise ValueError("Other user must exist (created in conftest.py)")

        # Reassign post to other user
        post = sqla.session.get(Post, test_post)
        post.author_id = other_user.id
        sqla.session.commit()

    resp_update = client.post(f"/blogs/{test_post}/update", follow_redirects=False)
    resp_delete = client.post(f"/blogs/{test_post}/delete", follow_redirects=False)
    assert resp_update.status_code == 403
    assert resp_delete.status_code == 403

def test_exists_required(client, auth):

    """Updating/deleting non-existent posts returns 404."""

    auth.login()
    for path in ("/blogs/999/update", "/blogs/999/delete"):

        response = client.post(path, follow_redirects=False)
        assert response.status_code == 404

def test_create(client, auth, app):

    """A logged-in user can create posts."""

    auth.login()
    response = client.post("/blogs/create", data={"title": "created", "body": "new body"}, follow_redirects=False)
    assert response.status_code == 302

    with app.app_context():

        post = sqla.session.query(Post).filter_by(title="created").first()
        assert post is not None
        assert post.body == "new body"

def test_update(client, auth, app, test_post):

    """A logged-in user can update their post."""

    auth.login()
    response = client.post(
        f"/blogs/{test_post}/update",
        data={"title": "updated", "body": "updated body"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"updated" in response.data

    with app.app_context():

        post = sqla.session.get(Post, test_post)
        assert post.title == "updated"

def test_create_update_validate(client, auth):

    """Title is required on create and update."""

    auth.login()
    response = client.post("/blogs/create", data={"title": "", "body": "body"}, follow_redirects=True)
    assert b"Title is required." in response.data

def test_delete(client, auth, app, test_post):

    """A logged-in user can delete their post."""

    auth.login()
    response = client.post(f"/blogs/{test_post}/delete", follow_redirects=False)
    assert response.status_code == 302

    with app.app_context():
        
        post = sqla.session.get(Post, test_post)
        assert post is None
