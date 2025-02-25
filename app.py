from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Cart

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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