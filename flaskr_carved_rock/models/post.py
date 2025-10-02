
# post.py

from datetime import datetime, timezone
from sqlalchemy.orm import validates

from flaskr_carved_rock.sqla import sqla


class Post(sqla.Model):
    
    id = sqla.Column(sqla.Integer, primary_key=True)
    author_id = sqla.Column(
        sqla.Integer,
        sqla.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )
    created = sqla.Column(
        sqla.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    title = sqla.Column(sqla.Text, nullable=False)
    body = sqla.Column(sqla.Text, nullable=False)

    @validates('title')
    def validate_not_empty(self, key, value):

        if not value:

            raise ValueError(f'{key.capitalize()} is required.')
        
        return value

    def __repr__(self):
        
        return self.title
