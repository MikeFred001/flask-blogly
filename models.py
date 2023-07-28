"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = """https://www.thetimes.co.uk/imageserver/image/
%2Fmethode%2Ftimes%2Fprodmigration%2Fweb%2Fbin%2F5ca5cbde-984c-328c-9
7f5-3805b28ebb87.jpg?crop=1500%2C1000%2C0%2C0"""
# Concat URL

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Contains descriptions and functionality for a User"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = db.Column(
        db.String(25),
        nullable=False
    )

    last_name = db.Column(
        db.String(25),
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE_URL
    )


class Post(db.Model):
    """Contains descriptions and functionality for a User"""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(25),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    user = db.relationship('User', backref='posts')

    tags = db.relationship(
        'Tag', secondary='post_tags', backref='posts'
    )


class Tag(db.Model):
    """Contains descriptions and functionality for a User"""

    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(25),
        nullable=False,
        unique=True
    )


class PostTag(db.Model):
    """Contains descriptions and functionality for a User"""

    __tablename__ = "post_tags"

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True
    )
