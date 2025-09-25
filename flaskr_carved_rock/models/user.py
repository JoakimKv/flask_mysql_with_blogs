
# user.py


from uuid import uuid4
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr_carved_rock.sqla import sqla
from flask_login import UserMixin


class User(UserMixin, sqla.Model):

    id = sqla.Column(sqla.Integer, primary_key=True)
    uuid = sqla.Column(sqla.String(64), nullable=False, default=lambda: str(uuid4()))
    username = sqla.Column(sqla.String(150), nullable=False, unique=True)
    password = sqla.Column(sqla.String(255), nullable=False)
    api_key = sqla.Column(sqla.String(64), nullable=True)

    # Option 2: relationship in User only, cascade deletes posts automatically
    posts = sqla.relationship(
        'Post',
        backref='author',        # defines the backref here only
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    @validates('username', 'password')
    def validate_not_empty(self, key, value):

        if not value:

            raise ValueError(f'{key.capitalize()} is required.')

        if key == 'username':

            self.validate_unique(key, value, f'{value} already registered')

        if key == 'password' and not value.startswith("pbkdf2:sha256"):

            value = generate_password_hash(value)

        return value

    def validate_unique(self, key, value, error_message=None):

        if User.query.filter_by(**{key: value}).first() is not None:

            if not error_message:

                error_message = f'{key} must be unique.'

            raise ValueError(error_message)
        
        return value

    def correct_password(self, plaintext):

        return check_password_hash(self.password, plaintext)

    def get_id(self):

        return self.uuid  # use UUID for Flask-Login

    def __repr__(self):
        
        return self.username
