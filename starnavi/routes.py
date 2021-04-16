from flask import request, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from starnavi.db.models import db, User, Post, PostLike
from flask_login import login_required, login_user, current_user, LoginManager
from flask_bcrypt import Bcrypt

project = Blueprint('project', __name__)
login_manager = LoginManager()
bcrypt = Bcrypt()

jwt = JWTManager()


@project.route('/')
def index():
    return {'status': 200}, 200


@project.route('/login', methods=['POST'])
@login_manager.user_loader
def login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=request.json['email']).first()
    if not user:
        return {"message": "User doesn't exist"}
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        login_user(current_user)

        return {'access_token': access_token}


@project.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user = get_jwt_identity()
    return user, 200


@project.route('/register', methods=['POST'])
def register():
    print(request.json)
    params = request.json
    hashed_password = bcrypt.generate_password_hash(params['password']).decode('utf-8')
    new_user = User(email=params['email'], password=hashed_password, first_name=params['first_name'],
                    last_name=params['last_name'], birth_date=params['birth_date'])
    db.session.add(new_user)
    db.session.commit()

    return {'status': 200}


@project.route('/like/<int:post_id>', methods=['POST', 'DELETE'])
# @login_required
# @jwt_required
def like_action(post_id):
    user = User.query.filter_by(id=1).first_or_404()
    login_user(user)
    post = Post.query.filter_by(id=post_id).first_or_404()
    if request.method == 'POST':
        current_user.like_post(post)
        db.session.commit()
        return {'message': 'Liked a post'}
    if request.method == 'DELETE':
        current_user.unlike_post(post)
        db.session.commit()
        return {'message': 'Unliked a post'}


@project.route('/newpost', methods=['POST'])
def create_post():
    user = User.query.filter_by(id=1).first()
    login_user(user)
    post = Post(title=request.json['title'], body=request.json['body'], user_id=current_user.id)
    db.session.add(post)
    db.session.commit()

    return {'status': 200}, 200


@project.route('/api/analytics', methods=['GET'])
def like_count():
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

    return f'{count}'
