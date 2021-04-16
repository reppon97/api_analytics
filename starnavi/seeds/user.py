from flask_seeder import FlaskSeeder, Seeder, Faker, generator
from starnavi.db.models import User
from starnavi.resolvers import bcrypt

seeder = FlaskSeeder()


class UserSeeder(Seeder):
    def __init__(self):
        super().__init__()
        print("Initializing User Faker")
        self.emails = set()

    def run(self):
        # Create a new Faker and tell it how to create User objects
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
            self.db.session.add(user)

        self.db.session.commit()
