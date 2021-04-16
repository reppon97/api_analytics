from flask import Flask
from starnavi.db.models import db, migrate
from starnavi.config import Config
from starnavi.routes import project, login_manager, jwt


app = Flask(__name__)
app.register_blueprint(project)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

jwt.init_app(app)

login_manager.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
