from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False) 
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)  
    date_added = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return f"<OrderItem {self.product_name}, Qty: {self.quantity}, Price: {self.price:.2f}>"
