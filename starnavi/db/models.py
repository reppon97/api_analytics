from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model, UserMixin):
    __tablename__ = 'api_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False, index=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(50), nullable=False, index=True)
    last_name = db.Column(db.String(50), nullable=False, index=True)
    birth_date = db.Column(db.Date, nullable=False, index=True)

    posts = db.relationship('Post', backref='author', lazy=True)
    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def __init__(self, email, password, first_name, last_name, birth_date):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    def __repr__(self):
        return f'User {self.first_name} {self.last_name}, Email: {self.email}'


class Post(db.Model):
    __tablename__ = 'api_post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, index=True)
    body = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('api_user.id'), nullable=False)

    likes = db.relationship('PostLike', backref='post', lazy='dynamic')

    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id

    def __repr__(self):
        return f'Post {self.title} by {self.user_id}'


class PostLike(db.Model):
    __tablename__ = 'post_like'

    id = db.Column(db.Integer, primary_key=True)
    date_liked = db.Column(db.Date, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('api_user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('api_post.id'))

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
