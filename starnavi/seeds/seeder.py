from flask_seeder import FlaskSeeder, Seeder, Faker, generator
from starnavi.db.models import User, PostLike, Post, db
from starnavi.resolvers import bcrypt
from random import randint


seeder = FlaskSeeder()
fake = Faker()


class UserSeeder(Seeder):
    def __init__(self):
        super().__init__()
        print("Initializing User Faker")
        self.emails = set()

    def run(self):
        faker = Faker(
            cls=User,
            init={
                "first_name": generator.Name(),
                "last_name": generator.Name(),
                "email": generator.String('[a-z][a-z]\d\d[a-z][a-z][a-z]@gmail.com'),
                "password": bcrypt.generate_password_hash(f'test123').decode('utf-8'),
                "birth_date": '2000-12-12'
            }
        )

        for user in faker.create(1_000):
            print(f"Adding user: {user}")
            db.session.add(user)

        db.session.commit()

        faker = Faker(
            cls=Post,
            init={
                "title": "Lorem ipsum dolor sit amet",
                "body": "consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna "
                             "aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut "
                             "aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate "
                             "velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non "
                             "proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
                "user_id": randint(1, 999),
            }
        )

        for post in faker.create(1000):
            print(f"Adding post: {post}")
            self.db.session.add(post)

        self.db.session.commit()
        faker = Faker(
            cls=PostLike,
            init={
                "user_id": randint(1, 999),
                "post_id": randint(1, 999),
                "date_liked": generator.String(f'{randint(2019, 2020)}-{randint(1, 12)}-{randint(1, 30)}')
            }
        )

        for like in faker.create(800):
            print(f"Adding like: {like.date_liked}")
            self.db.session.add(like)

        self.db.session.commit()
