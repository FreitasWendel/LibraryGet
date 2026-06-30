from flask import Flask
from src.models import db
from src.controllers import register_blueprints

def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config['SECRET_KEY'] = 'senha'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app