from flask import request, jsonify
from flask_restful import Resource
from database import db
from models import Product

class ProductDisplayResource(Resource):
    def get(self):
        """Publicly accessible endpoint for viewing all products."""
        products = Product.query.all()
        return ([product.to_dict() for product in products]), 200

    def post(self):
        """Allow anyone to create a new product (No authentication required)."""
        data = request.get_json()
        required_fields = {"name", "price", "description", "image", "category"}
        if not data or not required_fields.issubset(data.keys()):
            return {"error": "Missing required fields"}, 400

        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()

        return new_product.to_dict(), 201

class ProductResource(Resource):
    def get(self, id):
        """Publicly accessible: View a single product."""
        product = Product.query.get(id)
        return product.to_dict(), 200 if product else ({"error": "Product not found"}, 404)

    def patch(self, id):
        """Allow anyone to update a product (No authentication required)."""
        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404

        data = request.get_json()
        for key, value in data.items():
            setattr(product, key, value)

        db.session.commit()
        return product.to_dict(), 200

    def delete(self, id):
        """Allow anyone to delete a product (No authentication required)."""
        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404

        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}, 200
