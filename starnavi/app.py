from flask import Flask
from starnavi.db.models import db, migrate
from starnavi.config import Config
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS, cross_origin
from starnavi.resolvers import Resolver, jwt, login_manager
from starnavi.seeds.seeder import seeder


app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app, resources={r'/*': {'origins': '*'}})
api = Api(app)

db.init_app(app)
migrate.init_app(app, db)
seeder.init_app(app, db)

login_manager.init_app(app)
jwt.init_app(app)

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, help='Email of user')
parser.add_argument('password', type=str, help='Password of user')
parser.add_argument('first_name', type=str, help='First name of user')
parser.add_argument('last_name', type=str, help='Last name of user')
parser.add_argument('birth_date', type=str, help="User's date of birth")
parser.add_argument('title', type=str, help='Post title')
parser.add_argument('body', type=str, help='Post body')
parser.add_argument('user_id', type=int, help='User ID')
parser.add_argument('post_id', type=int, help='Post ID')


class UserSignUp(Resource):
    @cross_origin()
    def post(self):
        """
        POST /register
        :return:
        """
        args = parser.parse_args()
        return Resolver.register(args), 201


class UserLogin(Resource):
    @cross_origin()
    def post(self):
        """
        POST /login
        :return:
        """
        args = parser.parse_args()
        return Resolver.login(args), 200


class Post(Resource):
    @cross_origin()
    def post(self):
        """
        POST /newpost
        :return:
        """
        args = parser.parse_args()
        return Resolver.create_post(args), 201


class Like(Resource):
    @cross_origin()
    def post(self):
        """
        POST /like/<post_id>
        :return:
        """
        args = parser.parse_args()
        return Resolver.like(args), 200

    @cross_origin()
    def delete(self):
        """
        DELETE /like/<post_id>
        :return:
        """
        args = parser.parse_args()
        return Resolver.like(args), 204

    @cross_origin()
    def get(self):
        """
        GET /api/analytics/<date_from>&<date_to>
        :return:
        """
        return Resolver.analytics(), 200


api.add_resource(UserSignUp, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(Post, "/newpost")
api.add_resource(Like, "/like", "/api/analytics")


if __name__ == '__main__':
    app.run(debug=True)
