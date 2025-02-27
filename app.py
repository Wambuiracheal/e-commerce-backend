import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, OrderItem, Cart, User
from resources.shop import ProductDisplayResource, ProductResource
from resources.shop import RegisterResource, UserResource  

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
    api.add_resource(RegisterResource, '/register')
    api.add_resource(UserResource, '/user')
    # api.add_resource()
    
    @app.route('/')
    def home():
        return (
            '<h1>Welcome to ShopIT</h1>'
            '<p>Where quality meets affordability</p>'
        )

    @app.route('/order_items', methods=['GET'])
    def get_order_items():
        items = OrderItem.query.all()
        return jsonify([{
            'id': item.id,
            'order_id': item.order_id,
            'product_name': item.product_name,
            'quantity': item.quantity,
            'price': item.price  
        } for item in items])

    @app.route('/order_items/<int:item_id>', methods=['GET'])
    def get_order_item(item_id):
        item = OrderItem.query.get(item_id)
        if not item:
            return jsonify({"error": "Order item not found"}), 404

        return jsonify({
            'id': item.id,
            'order_id': item.order_id,
            'product_name': item.product_name,
            'quantity': item.quantity,
            'price': item.price  
        })

    @app.route('/order_items', methods=['POST'])
    def create_order_item():
        data = request.json
        new_item = OrderItem(
            order_id=data['order_id'],
            product_name=data['product_name'],
            quantity=data['quantity'],
            price=data['price']
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({
            'message': 'Order item added successfully',
            'id': new_item.id,
            'price': new_item.price  
        }), 201


    @app.route('/cart', methods=['GET'])
    def get_cart():
        cart_items = Cart.query.all()
        return jsonify([item.to_dict() for item in cart_items]), 200

    @app.route('/cart', methods=['POST'])
    def add_to_cart():
        data = request.get_json()
        new_cart_item = Cart(
            user_id=data['user_id'],
            product_id=data['product_id'],
            quantity=data.get('quantity', 1)
        )
        db.session.add(new_cart_item)
        db.session.commit()
        return jsonify(new_cart_item.to_dict()), 201

    @app.route('/cart/<int:cart_id>', methods=['DELETE'])
    def delete_cart_item(cart_id):
        cart_item = Cart.query.get(cart_id)
        if not cart_item:
            return jsonify({"error": "Cart item not found"}), 404

        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Cart item removed"}), 200
    
    return app
# abdi


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5555)
    # app.run(host='0.0.0.0', port=os.environ.get('PORT', 5555))
