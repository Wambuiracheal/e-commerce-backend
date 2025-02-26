from flask import Flask, request, jsonify
from models import db, OrderItem
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

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
