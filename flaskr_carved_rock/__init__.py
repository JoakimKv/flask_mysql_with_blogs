
# __init__.py


import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from flaskr_carved_rock.sqla import sqla
from flaskr_carved_rock.database_connection_data import DatabaseConnectionData


login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # redirect unauthorized users to login


def create_app(testing=False):

    """Create and configure the Flask application."""

    # --- Database setup ---
    databaseConnectionData = DatabaseConnectionData(testing=testing)
    username = databaseConnectionData.username
    password = databaseConnectionData.password
    database = databaseConnectionData.database
    host = databaseConnectionData.host
    port = databaseConnectionData.port
    sslDisabled = databaseConnectionData.sslDisabled
    sslParam = "ssl=true" if not sslDisabled else "ssl_disabled=true"

    if not username or not password:

        raise RuntimeError("MySQL credentials not set in environment variables.")

    # --- App creation ---
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
        static_url_path="/blogs/static",
    )

    app.url_map.strict_slashes = False

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY_BLOGS", "dev"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTING=testing,
        SQLALCHEMY_DATABASE_URI=(
            f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?{sslParam}"
        ),
    )

    # Respect proxy headers for HTTPS & host.

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    app.config["PREFERRED_URL_SCHEME"] = "https" if not app.debug else "http"

    # Django base URL.

    app.config["DJANGO_URL"] = (
        "https://kvistholm.net/" if not app.debug else "http://localhost:8000/"
    )

    # --- Setup paths ---

    try:

        os.makedirs(app.instance_path)

    except OSError:

        pass

    # --- Init login + DB ---

    login_manager.init_app(app)

    from flaskr_carved_rock.models.user import User

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.filter_by(uuid=user_id).first()

    from flaskr_carved_rock import db

    db.init_app(app)
    sqla.init_app(app)

    # --- Blueprints ---

    from flaskr_carved_rock import auth, blog

    app.register_blueprint(auth.bp, url_prefix="/blogs")
    app.register_blueprint(blog.bp, url_prefix="/blogs")

    # --- Context for templates ---

    @app.context_processor
    def inject_django_url():

        return {"DJANGO_URL": app.config["DJANGO_URL"]}

    # --- Routes ---
    @app.route("/")
    def root():

        """Redirect base domain to Django."""

        return redirect(app.config["DJANGO_URL"])

    # Blog index is served by the blog blueprint mounted at /blogs/

    @app.route("/hello")
    def hello():
        
        return "Hello, World!", 200, {"Content-Type": "text/plain"}

    return app
