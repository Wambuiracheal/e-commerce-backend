from flask import request
from flask_restful import Resource
from models import Product, Cart, db

# PROUDUCTS CRUD OPERATION 
class ProductDisplayResource(Resource):
    def get(self):
        products = Product.query.all()
        return([product.to_dict() for product in products]), 200
    
    def post(self):
        data = request.get_json()

        required_fields = {"name","price","description","url","category"}
        if not data or required_fields.issubset(data.keys()):
            return {"error": "Missing required fields"}, 400
        
        existing_product = Product.query.filter_by(name=data["name"]).first()
        if existing_product:
            return {"error": "Product already exists"}, 400
    
        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()

        return new_product.to_dict(), 201
    
class ProductResource(Resource):
    def get(self, id):

        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404
        return product.to_dict(), 200
        
    def patch(self, id):

        data = request.get_json()
        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404

        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            product.price = data['price']
        if 'description' in data:
            product.description = data['description']
        if 'url' in data:
            product.url = data['url']
        if 'category' in data:
            product.category = data['category']

        db.session.commit()
        return [product.to_dict()], 200

    def delete(self, id):

        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404

        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}, 200
    
# CART CRUD OPERATION
class CartDisplayResource(Resource):
    def get(self):
        """Get all cart items"""
        cart_items = Cart.query.all()
        return [item.to_dict() for item in cart_items], 200

    def post(self):
        """Add a new item to the cart"""
        data = request.get_json()

        if not data or "product_id" not in data or "quantity" not in data:
            return {"error": "Missing required fields"}, 400
        
        # Ensure product exists
        product = Product.query.get(data["product_id"])
        if not product:
            return {"error": "Product not found"}, 404

        # Check if product is already in cart
        existing_cart_item = Cart.query.filter_by(product_id=data["product_id"]).first()
        if existing_cart_item:
            existing_cart_item.quantity += data["quantity"]
            db.session.commit()
            return existing_cart_item.to_dict(), 200

        # Create a new cart item
        new_cart_item = Cart(**data)
        db.session.add(new_cart_item)
        db.session.commit()

        return new_cart_item.to_dict(), 201


class CartResource(Resource):
    def get(self, id):
        """Get a specific cart item"""
        cart_item = Cart.query.get(id)
        if not cart_item:
            return {"error": "Cart item not found"}, 404
        return cart_item.to_dict(), 200

    def patch(self, id):
        """Update quantity of a cart item"""
        data = request.get_json()
        cart_item = Cart.query.get(id)

        if not cart_item:
            return {"error": "Cart item not found"}, 404

        if 'quantity' in data and data["quantity"] > 0:
            cart_item.quantity = data["quantity"]
            db.session.commit()
            return cart_item.to_dict(), 200
        else:
            return {"error": "Invalid quantity"}, 400

    def delete(self, id):
        """Remove an item from the cart"""
        cart_item = Cart.query.get(id)
        if not cart_item:
            return {"error": "Cart item not found"}, 404

        db.session.delete(cart_item)
        db.session.commit()
        return {"message": "Cart item removed"}, 200
