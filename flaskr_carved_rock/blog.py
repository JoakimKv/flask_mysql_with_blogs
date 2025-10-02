
# blog.py


from flask import Blueprint, flash, g, redirect
from flask import render_template, request, url_for
from werkzeug.exceptions import abort

from flask_login import login_required
from flaskr_carved_rock.models import Post
from flaskr_carved_rock.sqla import sqla
from flask_login import current_user


bp = Blueprint("blog", __name__)


@bp.route("/")
def index():

    """Show all the posts, most recent first."""

    posts = Post.query.all()
    return render_template("blog/index.html", posts=posts)


def get_post(id, check_author=True):

    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """

    post = Post.query.filter_by(id=id).first()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != current_user.id:
        abort(403)

    return post

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():

    """Create a new post for the current user."""

    if request.method == "POST":

        try:

            post = Post(title=request.form["title"], body=request.form["body"], author_id=current_user.id)

        except ValueError as e:

            # failed validation, so flash the message to the user
            flash(str(e))
            return render_template("blog/create.html")

        # Post was validated, so save to DB and return to index
        sqla.session.add(post)
        sqla.session.commit()
        return redirect(url_for("blog.index"))

    return render_template("blog/create.html")

@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):

    """Update a post if the current user is the author."""

    post = get_post(id)

    if request.method == "POST":
        try:
            post.title = request.form["title"]
            post.body = request.form["body"]
        except ValueError as e:
            flash(e)
            return render_template("blog/update.html", post=post)

        sqla.session.add(post)
        sqla.session.commit()
        return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)

@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):

    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    post = get_post(id)
    sqla.session.delete(post)
    sqla.session.commit()
    
    return redirect(url_for("blog.index"))
