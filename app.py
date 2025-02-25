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
        'price': f"Ksh {item.price:.2f}"
    } for item in items])

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
    return jsonify({'message': 'Order item added successfully', 'price': f"Ksh {new_item.price:.2f}"}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
