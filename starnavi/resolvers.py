from starnavi.db.models import db, User, Post, PostLike
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask import request

bcrypt = Bcrypt()
jwt = JWTManager()


class UserResolver:
    @staticmethod
    def register(params):
        hashed_password = bcrypt.generate_password_hash(params['password']).decode('utf-8')
        new_user = User(email=params['email'], password=hashed_password, first_name=params['first_name'],
                        last_name=params['last_name'], birth_date=params['birth_date'])
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'success'}

    @staticmethod
    def login(params):
        email = params['email']
        password = params['password']
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "User doesn't exist"}
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=email)

            return {'message': 'success', 'access_token': access_token}

    @staticmethod
    def create_post(params):
        user = User.query.filter_by(id=params['user_id']).first()
        post = Post(title=params['title'], body=params['body'], user_id=user.id)
        db.session.add(post)
        db.session.commit()

        return {'message': 'success'}

    @staticmethod
    def like(params):
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
