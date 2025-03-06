from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

# ADMIN
class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# USERS
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum('buyer', 'seller', 'admin', name='user_roles'), nullable=False, default='buyer')

    orders = db.relationship("Order", backref="user", lazy=True)
    cart_items = db.relationship("Cart", backref="user", lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# SELLERS
class Seller(db.Model, SerializerMixin):
    __tablename__ = 'sellers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    store_name = db.Column(db.String(100), nullable=False)

    products = db.relationship("Product", backref="seller", lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# PRODUCTS
class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

    cart_items = db.relationship('Cart', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)


# ORDERS
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="unpaid")
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    order_items = db.relationship("OrderItem", backref="order", lazy=True)
    payment = db.relationship("Payment", uselist=False, backref="order")


# ORDER ITEMS
class OrderItem(db.Model, SerializerMixin):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<OrderItem {self.product_name}, Qty: {self.quantity}, Price: {self.price:.2f}>"


# PAYMENTS
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, unique=True)
    payment_method = db.Column(db.Enum('card', 'paypal', 'bank_transfer', name='payment_methods'), nullable=False)
    status = db.Column(db.Enum('pending', 'successful', 'failed', name='payment_status'), nullable=False, default='pending')
    transaction_id = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# CART
class Cart(db.Model, SerializerMixin):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    product = db.relationship("Product", backref="cart_items")  # Added for easy product access

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "product_name": self.product.name,
            "price": self.product.price,
        }

