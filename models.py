from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# PRODUCTS
def Product():
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(35), nullable=False)
    price = db.Column(db.Float, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(35), nullable=False)