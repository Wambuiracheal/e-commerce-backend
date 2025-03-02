from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from models import db, Order, Product, User

# PRODUCTS CRUD OPERATION 
class ProductDisplayResource(Resource):
    def get(self):
        products = Product.query.all()
        return([product.to_dict() for product in products]), 200
    
    def post(self):
        data = request.get_json()

        required_fields = {"name","price","description","image","category"}
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
        if 'image' in data:
            product.image = data['image']
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
   
    #ORDER CRUD OPERATIONS
class OrderDisplayResource(Resource):
    def get(self):
        orders = Order.query.all()
        return [order.to_dict() for order in orders], 200
    
    def post(self):
        data = request.get_json()
        required_fields = {"full_name", "address", "city", "payment_method", "total_amount"}
        
        if not data or not required_fields.issubset(data.keys()):
            return {"error": "Missing required fields"}, 400
        
        new_order = Order(
            full_name=data["full_name"],
            address=data["address"],
            city=data["city"],
            payment_method=data["payment_method"],
            total_amount=data["total_amount"],
            status=data.get("status", "unpaid")
        )

        db.session.add(new_order)
        db.session.commit()
        return new_order.to_dict(), 201


class OrderResource(Resource):
    def get(self, id):
        order = Order.query.get(id)
        if not order:
            return {"error": "Order not found"}, 404
        
        return order.to_dict(), 200
    
    def patch(self, id):
        order = Order.query.get(id)
        if not order:
            return {"error": "Order not found"}, 404
        
        data = request.get_json()

        if 'full_name' in data:
            order.full_name = data['full_name']
        if 'address' in data:
            order.address = data['address']
        if 'city' in data:
            order.city = data['city']
        if 'payment_method' in data:
            order.payment_method = data['payment_method']
        if 'total_amount' in data:
            order.total_amount = data['total_amount']
        if 'status' in data:
            order.status = data['status']

        db.session.commit()
        return order.to_dict(), 200

    def delete(self, id):
        order = Order.query.get(id)
        if not order:
            return {"error": "Order not found"}, 404
        
        db.session.delete(order)
        db.session.commit()
        return {"message": "Order deleted successfully"}, 200

# USERS CRUD OPERATION
class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        hashed_password = generate_password_hash(data['password']).decode('utf-8')
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            role=data['role']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201


class UserResource(Resource):
    @jwt_required()
    def patch(self):
        user = get_jwt_identity()
        user_info = User.query.get(user['id'])

        if not user_info:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        if 'name' in data:
            user_info.name = data['name']
        if 'email' in data:
            user_info.email = data['email']

        db.session.commit()
        return jsonify({'message': 'User updated successfully'})

    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        user_info = User.query.get(user['id'])

        if not user_info:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'id': user_info.id,
            'name': user_info.name,
            'email': user_info.email,
            'role': user_info.role
        })
