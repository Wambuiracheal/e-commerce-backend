<<<<<<< HEAD
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
=======
from flask_restful import Api
from models import db
from flask_cors import CORS
from flask import Flask, request, jsonify
from models import db, OrderItem,Cart
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

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

@app.route('/order_items/<int:item_id>', methods=['PUT'])
def update_order_item(item_id):
    item = OrderItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Order item not found"}), 404

    data = request.json
    item.order_id = data['order_id']
    item.product_name = data['product_name']
    item.quantity = data['quantity']
    item.price = data['price']

    db.session.commit()
    return jsonify({"message": "Order item updated successfully"})

@app.route('/order_items/<int:item_id>', methods=['PATCH'])
def patch_order_item(item_id):
    item = OrderItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Order item not found"}), 404

    data = request.json
    if 'order_id' in data:
        item.order_id = data['order_id']
    if 'product_name' in data:
        item.product_name = data['product_name']
    if 'quantity' in data:
        item.quantity = data['quantity']
    if 'price' in data:
        item.price = data['price']

    db.session.commit()

@app.route('/order_items/<int:item_id>', methods=['DELETE'])
def delete_order_item(item_id):
    item = OrderItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Order item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Order item deleted successfully"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], email=data['email'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/user', methods=['PATCH'])
@jwt_required()
def update_user():
    user = get_jwt_identity()
    user_info = User.query.get(user['id'])
    if not user_info:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    if 'name' in data:
        user_info.name = data['name']
    if 'email' in data:
        user_info.email = data['email']

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    user = get_jwt_identity()
    user_info = User.query.get(user['id'])
    if user_info:
        return jsonify({'id': user_info.id, 'name': user_info.name, 'email': user_info.email, 'role': user_info.role})
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

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
        quantity=data.get['quantity', 1]
    )
    db.session.add(new_cart_item)
    db.session.commit()
    return jsonify(new_cart_item.to_dict()), 201

@app.route('/cart/<int:cart_id>', methods=['PATCH'])
def update_cart_item(cart_id):
    cart_item = Cart.query.get(cart_id)
    if not cart_item:
        return jsonify({"error": "Cart item not found"}), 404

    data = request.get_json()
    cart_item.quantity = data.get("quantity", cart_item.quantity)
    db.session.commit()
    return jsonify(cart_item.to_dict()), 200

@app.route('/cart/<int:cart_id>', methods=['DELETE'])
def delete_cart_item(cart_id):
    cart_item = Cart.query.get(cart_id)
    if not cart_item:
        return jsonify({"error": "Cart item not found"}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Cart item removed"}), 200

if __name__ == '__main__':
    app.run(debug=True)

>>>>>>> d0f6e98f5a1d807ff5ccdd47d569587954df3f27
