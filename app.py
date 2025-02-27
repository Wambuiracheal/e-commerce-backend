from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from models import db, Cart
import os

app = Flask(__name__)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = FALSE
migrate = Migrate(app, db)

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

