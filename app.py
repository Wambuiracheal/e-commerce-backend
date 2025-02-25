import os
from models import db
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = '///sqlite:shopit.db'
    app.config['SQLALCHEMY_MODIFICATION'] = False

    migrate = Migrate(app,db)
    app = CORS(app)

    db.init_app(app)
    app = Api(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return (
            '<h1>Welcome to the shopIT</h1>'
            '<p>Where quality meets affordability</p>'
        )
            

    return app


