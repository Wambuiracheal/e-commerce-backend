import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, OrderItem, Cart, User
from resources.shop import ProductDisplayResource, ProductResource, CartDisplayResource, CartResource


def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopit.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    
    with app.app_context():
        db.create_all()
    
    api.add_resource(ProductDisplayResource, '/products')
    api.add_resource(ProductResource, '/products/<int:id>')
    api.add_resource(CartDisplayResource, '/cart')
    api.add_resource(CartResource, '/cart/<int:id>')
    # api.add_resource()
    
    @app.route('/')
    def home():
        return (
            '<h1>Welcome to ShopIT</h1>'
            '<p>Where quality meets affordability</p>'
        )
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5555)
