
# __init__.py


import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from flaskr_carved_rock.sqla import sqla

from flaskr_carved_rock.database_connection_data import DatabaseConnectionData
from .secret_vault_class import SecretVault


secretVault = SecretVault()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # redirect unauthorized users to login


def create_app(testing = False):

    """Create and configure the Flask application."""
           
    databaseConnectionData = DatabaseConnectionData(testing = testing)

    username = databaseConnectionData.username
    password = databaseConnectionData.password
    database = databaseConnectionData.database
    host = databaseConnectionData.host
    port = databaseConnectionData.port
    sslDisabled = databaseConnectionData.sslDisabled

    sslParam = "ssl=true" if not sslDisabled else "ssl_disabled=true"    

    if not username or not password:

        raise RuntimeError("MySQL credentials not set in environment variables.")

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
        static_url_path="/blogs/static"
    )

    app.url_map.strict_slashes = False

    app.config.from_mapping(
        SECRET_KEY = os.getenv("SECRET_KEY_BLOGS", "dev"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        TESTING = testing,
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?{sslParam}"
    )

    # Respect proxy headers for correct URL generation
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    # Prefer https in production for external URL generation
    app.config["PREFERRED_URL_SCHEME"] = "https" if not app.debug else "http"

   # Dynamic link back to Django app (for templates).
    app.config["DJANGO_URL"] = (
        "https://kvistholm.net/"
        if not secretVault.getDebugMode()
        else "http://localhost:8000/"
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize login manager
    login_manager.init_app(app)

    # User loader with UUID
    from flaskr_carved_rock.models.user import User

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.filter_by(uuid = user_id).first()

    # Initialize database commands
    from flaskr_carved_rock import db
    db.init_app(app)

    # Initialize SQLAlchemy
    sqla.init_app(app)

    # Register blueprints
    from flaskr_carved_rock import auth, blog
    # Mount blog under /blogs and auth under /blogs/auth (auth bp already has /auth prefix)
    app.register_blueprint(auth.bp, url_prefix="/blogs")
    app.register_blueprint(blog.bp, url_prefix="/blogs")

    # Make DJANGO_URL globally available in templates.
    @app.context_processor
    def inject_django_url():
        
        return {"DJANGO_URL": app.config["DJANGO_URL"]}

    # Root: redirect to Django site
    @app.route("/")
    def root():

        return redirect(app.config["DJANGO_URL"])  # 302 by default

    # Blogs index: serve Flask blog
    @app.route("/blogs")
    def index():

        return render_template("blog/index.html")

    # Optional route for testing
    @app.route("/hello")
    def hello():
        
        return "Hello, World!", 200, {"Content-Type": "text/plain"}

    return app
