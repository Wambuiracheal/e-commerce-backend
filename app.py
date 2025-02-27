import os
from models import db
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from resources.shop import ProductDisplayResource, ProductResource


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopit.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    migrate = Migrate(app,db)
    CORS(app)

    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.add_resource(ProductDisplayResource, '/products')
    api.add_resource(ProductResource,'/products/<int:id>')

    @app.route('/')
    def home():
        return (
            '<h1>Welcome to the shopIT</h1>'
            '<p>Where quality meets affordability</p>'
        )
            
    if __name__ == '__main__':
        app.run(debug=True)

    return app
