from flask import request, jsonify
from flask_restful import Resource
from models import Product, User, db
from flask_jwt_extended import jwt_required, get_jwt_identity

class ProductDisplayResource(Resource):
    def get(self):
        """Publicly accessible endpoint for viewing all products."""
        products = Product.query.all()
        return ([product.to_dict() for product in products]), 200

    @jwt_required()
    def post(self):
        """Restricted to admins: Create a new product."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != "admin":  # Ensure only admins can create products
            return {"error": "Unauthorized. Only admins can add products."}, 403

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

    @jwt_required()
    def patch(self, id):
        """Restricted to admins: Update a product."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != "admin":
            return {"error": "Unauthorized. Only admins can update products."}, 403

        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404

        data = request.get_json()
        for key, value in data.items():
            setattr(product, key, value)

        db.session.commit()
        return product.to_dict(), 200

    @jwt_required()
    def delete(self, id):
        """Restricted to admins: Delete a product."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != "admin":
            return {"error": "Unauthorized. Only admins can delete products."}, 403

        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404

        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}, 200