
# auth.py


from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import login_user, logout_user
from flask_login import login_required, current_user
from urllib.parse import urlparse, urljoin

from flaskr_carved_rock.models import User
from flaskr_carved_rock.sqla import sqla


bp = Blueprint("auth", __name__, url_prefix="/auth")


def is_safe_redirect_url(target):

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@bp.route("/register", methods=("GET", "POST"))
def register():

    """Register a new user."""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        try:

            user = User(username=username, password=password)
            sqla.session.add(user)
            sqla.session.commit()

        except ValueError as e:

            flash(str(e))
            return render_template("auth/register.html")

        flash("Registration successful. Please log in.")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@bp.route("/delete_account", methods=("GET", "POST"))
@login_required
def delete_account():

    """Allow the logged-in user to delete their own account."""

    if request.method == "POST":

        try:

            # Fetch the current user from DB
            user = sqla.session.get(User, current_user.id)
            if not user:
                flash("User not found.")
                return redirect(url_for("blog.index"))

            # Ensure user is deleting their own account
            if user.id != current_user.id:
                flash("You cannot delete another user's account.")
                return redirect(url_for("blog.index"))

            # Delete user and cascade posts
            sqla.session.delete(user)
            sqla.session.commit()

            logout_user()
            flash("Your account has been deleted permanently.")
            return redirect(url_for("blog.index"))

        except Exception as e:

            sqla.session.rollback()
            flash(f"Error deleting account: {str(e)}")
            return redirect(url_for("auth.delete_account"))

    # GET: show confirmation page
    return render_template("auth/delete_account.html")

@bp.route("/change_password", methods=("GET", "POST"))
@login_required
def change_password():

    """Allow the logged-in user to change their password."""

    if request.method == "POST":

        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # Fetch user from the DB
        user = sqla.session.get(User, current_user.id)

        if not user:

            flash("User not found.")
            return redirect(url_for("blog.index"))

        # Verify old password
        if not user.correct_password(current_password):

            flash("Current password is incorrect.")
            return redirect(url_for("auth.change_password"))

        # Ensure new password matches confirmation
        if new_password != confirm_password:

            flash("New passwords do not match.")
            return redirect(url_for("auth.change_password"))

        # Update password securely
        try:

            user.password = new_password  # triggers hash in User model validate
            sqla.session.commit()
            flash("Password updated successfully.")
            return redirect(url_for("blog.index"))
        
        except Exception as e:

            sqla.session.rollback()
            flash(f"Error updating password: {str(e)}")
            return redirect(url_for("auth.change_password"))

    return render_template("auth/change_password.html")

@bp.route("/login", methods=("GET", "POST"))
def login():

    """Log in a registered user."""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        user = User.query.filter_by(username=username).first()
        if user is None:
            error = "Incorrect username."
        elif not user.correct_password(password):
            error = "Incorrect password."

        if error:
            flash(error)
            return render_template("auth/login.html")

        login_user(user)

        next_url = request.args.get("next")
        if next_url and not is_safe_redirect_url(next_url):
            return abort(400)

        return redirect(next_url or url_for("blog.index"))

    return render_template("auth/login.html")

@bp.route("/logout")
def logout():

    """Log out the current user."""
    
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))
