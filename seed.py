from app import app, db
from models import Cart

with app.app_context():
    cart_items = [
        Cart(user_id=1, product_id=101, quantity=2),
        Cart(user_id=2, product_id=102, quantity=1),
        Cart(user_id=1, product_id=103, quantity=5),
    ]

    db.session.add_all(cart_items)
    db.session.commit()

    print("Database seeded successfully!")