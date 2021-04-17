from starnavi.db.models import db, User, Post, PostLike
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask import request
from flask_login import LoginManager, login_user, current_user

login_manager = LoginManager()
bcrypt = Bcrypt()
jwt = JWTManager()


class Resolver:
    @staticmethod
    def register(params):
        """
        User register method
        :param params: email, password, first name, last_name, birthday
        :return:
        """
        hashed_password = bcrypt.generate_password_hash(params['password']).decode('utf-8')
        new_user = User(email=params['email'], password=hashed_password, first_name=params['first_name'],
                        last_name=params['last_name'], birth_date=params['birth_date'])
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'success'}

    @staticmethod
    def login(params):
        """
        User login method
        :param params: email, password
        :return: JWT access key
        """
        email = params['email']
        password = params['password']
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "User doesn't exist"}
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            access_token = create_access_token(identity=email)

            return {'message': 'success', 'access_token': access_token}

    @staticmethod
    @jwt_required
    def protected():
        return {'message': 'This is protected'}

    @staticmethod
    def create_post(params):
        """
        Create Post method
        :param params: user id, post title and body
        :return:
        """
        user = User.query.filter_by(id=params['user_id']).first()
        post = Post(title=params['title'], body=params['body'], user_id=user.id)
        db.session.add(post)
        db.session.commit()

        return {'message': 'success'}

    @staticmethod
    def like(params):
        """
        Post Like/Dislike method
        :param params: user id, post id
        :return:
        """
        user = User.query.filter_by(id=params['user_id']).first()
        post = Post.query.filter_by(id=params['post_id']).first()
        if request.method == 'POST':
            user.like_post(post)
            db.session.commit()
            return {'message': 'success'}

        elif request.method == 'DELETE':
            user.unlike_post(post)
            db.session.commit()

            return {'message': 'success'}

    @staticmethod
    def analytics():
        """
        Analytics about how many likes were made in selected date range
        :return:
        """
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')

        post_like = PostLike.query
        if date_to and date_from:
            post_like = post_like.filter(PostLike.date_liked.between(date_from, date_to))
        elif date_to:
            post_like = post_like.filter(PostLike.date_liked <= date_to)
        elif date_from:
            post_like = post_like.filter(PostLike.date_liked >= date_from)
        count = post_like.count()

        return {'like_count': count}
