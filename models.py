from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False) 

    def __repr__(self):
        return f"<OrderItem {self.product_name}, Qty: {self.quantity}, Price: Ksh {self.price:.2f}>"
