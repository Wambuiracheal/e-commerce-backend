from flask import request
from flask_restful import Resource
from models import Product,db

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
