
# __init__.py


import os
from flask import Flask, render_template
from flask_login import LoginManager
from flaskr_carved_rock.sqla import sqla

from flaskr_carved_rock.database_connection_data import DatabaseConnectionData


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
        static_folder=os.path.join(os.path.dirname(__file__), "static")
    )

    app.config.from_mapping(
        SECRET_KEY = os.getenv("SECRET_KEY_BLOGS", "dev"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        TESTING = testing,
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?{sslParam}"
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

        return User.query.filter_by(uuid=user_id).first()

    # Initialize database commands
    from flaskr_carved_rock import db
    db.init_app(app)

    # Initialize SQLAlchemy
    sqla.init_app(app)

    # Register blueprints
    from flaskr_carved_rock import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # Index route
    @app.route("/")
    def index():

        return render_template("index.html", title = "Posts - Flaskr")

    # Optional route for testing
    @app.route("/hello")
    def hello():
        
        return "Hello, World!", 200, {"Content-Type": "text/plain"}

    return app
