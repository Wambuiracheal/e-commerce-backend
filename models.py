from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# PRODUCTS
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    
    cart_items = db.relationship('Cart', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

# # PAYMENTS
# class Payment(db.Model):
#     __tablename__ = 'payments'
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
#     payment_method = db.Column(db.Enum('card', 'paypal', 'bank_transfer', name='payment_methods'), nullable=False)
#     status = db.Column(db.Enum('pending', 'successful', 'failed', name='payment_status'), nullable=False, default='pending')
