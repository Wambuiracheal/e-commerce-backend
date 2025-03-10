from flask_restful import Resource
from flask import request,jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Order, Product, User

# PRODUCTS CRUD OPERATION 
class ProductDisplayResource(Resource):
    def get(self):
        products = Product.query.all()
        return [product.to_dict() for product in products]
    
    def post(self):
        data = request.get_json()

        required_fields = {"name","price","description","image","category"}
        if not data or not required_fields.issubset(data.keys()):
            return({"error": "Missing required fields"}), 400
        
        existing_product = Product.query.filter_by(name=data["name"]).first()
        if existing_product:
            return({"error": "Product already exists"}), 400
    
        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()
        print(new_product)
        return(new_product.to_dict()), 201
    
class ProductResource(Resource):
    def get(self, id):
        product = Product.query.get(id)
        if not product:
            return({"error": "Product not found"}), 404
        return(product.to_dict()), 200
        
    def patch(self, id):

        data = request.get_json()
        product = Product.query.get(id)
        if not product:
            return({"error": "Product not found"}), 404

        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            product.price = data['price']
        # if 'description' in data:
        #     product.description = data['description']
        # if 'image' in data:
        #     product.image = data['image']
        # if 'category' in data:
        #     product.category = data['category']

        db.session.commit()
        return(product.to_dict()), 200

    def delete(self, id):

        product = Product.query.get(id)
        if not product:
            return({"error": "Product not found"}), 404

        db.session.delete(product)
        db.session.commit()
        return({"message": "Product deleted"}), 200
   
# ORDER CRUD OPERATIONS
class OrderDisplayResource(Resource):
    def get(self):
        orders = Order.query.all()
        return([order.to_dict() for order in orders]), 200
    
    def post(self):
        data = request.get_json()
        required_fields = {"full_name", "address", "city", "payment_method", "total_amount"}
        
        if not data or not required_fields.issubset(data.keys()):
            return({"error": "Missing required fields"}), 400
        
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
        return(new_order.to_dict()), 201


class OrderResource(Resource):
    def get(self, id):
        order = Order.query.get(id)
        if not order:
            return({"error": "Order not found"}), 404
        
        return(order.to_dict()), 200
    
    def patch(self, id):
        order = Order.query.get(id)
        if not order:
            return({"error": "Order not found"}), 404
        
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
        return(order.to_dict()), 200

    def delete(self, id):
        order = Order.query.get(id)
        if not order:
            return({"error": "Order not found"}), 404
        
        db.session.delete(order)
        db.session.commit()
        return({"message": "Order deleted successfully"}), 200
# class BuyerDisplayResource(Resource):
#     def get(self):
#         # Retrieve all buyers
#         buyers = Buyer.query.all()
#         return [buyer.to_dict() for buyer in buyers], 200

#     def post(self):
#         # Create a new buyer
#         data = request.get_json()
        
#         required_fields = {"first_name", "last_name", "email", "address", "phone_number"}
#         if not data or not required_fields.issubset(data.keys()):
#             return {"error": "Missing required fields"}, 400
        
#         existing_buyer = Buyer.query.filter_by(email=data["email"]).first()
#         if existing_buyer:
#             return {"error": "Buyer already exists with this email"}, 400
        
#         new_buyer = Buyer(**data)
#         db.session.add(new_buyer)
#         db.session.commit()
#         return new_buyer.to_dict(), 201

# class BuyerResource(Resource):
#     def get(self, id):
#         # Retrieve a single buyer by ID
#         buyer = Buyer.query.get(id)
#         if not buyer:
#             return {"error": "Buyer not found"}, 404
#         return buyer.to_dict(), 200

#     def patch(self, id):
#         # Update buyer information
#         data = request.get_json()
#         buyer = Buyer.query.get(id)
#         if not buyer:
#             return {"error": "Buyer not found"}, 404

#         if 'first_name' in data:
#             buyer.first_name = data['first_name']
#         if 'last_name' in data:
#             buyer.last_name = data['last_name']
#         if 'email' in data:
#             buyer.email = data['email']
#         if 'address' in data:
#             buyer.address = data['address']
#         if 'phone_number' in data:
#             buyer.phone_number = data['phone_number']
        
#         db.session.commit()
#         return buyer.to_dict(), 200

#     def delete(self, id):
#         # Delete a buyer by ID
#         buyer = Buyer.query.get(id)
#         if not buyer:
#             return {"error": "Buyer not found"}, 404

#         db.session.delete(buyer)
#         db.session.commit()
#         return {"message": "Buyer deleted"}, 200


# USERS CRUD OPERATION

class RegisterResource(Resource):
    def post(self):
        try:
            data = request.get_json()

            print(f"Received data: {data}")

            if not data.get('name') or not data.get('email') or not data.get('password') or not data.get('role'):
                return {'message': 'Missing required fields'}, 400

            hashed_password = generate_password_hash(data['password'])
            print(f"Hashed password: {hashed_password}")

            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return {'message': 'Email already registered'}, 400

            new_user = User(
                name=data['name'],
                email=data['email'],
                password=hashed_password,  
                role=data['role']
            )

            db.session.add(new_user)
            db.session.commit()

            return {'message': 'User registered successfully'}, 201
        except Exception as e:
            print(f"Error during registration: {e}")
            return {'message': 'Internal server error'}, 500


class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"message": "No input data provided"}, 400

            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return {"message": "Email and password are required"}, 400

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.id)
                print(f"Generated Access Token: {access_token}")

                return {
                    "access_token": access_token,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "role": user.role  
                    }
                }, 200
            else:
                print("Invalid credentials")
                return {"message": "Invalid credentials"}, 401

        except Exception as e:
            print(f"Error during login: {str(e)}")
            return {"message": "Internal server error"}, 500

class UserResource(Resource):
    @jwt_required()
    def patch(self):
        user_id = get_jwt_identity()
        user_info = User.query.get(user_id)

        if not user_info:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()

        if 'email' in data:
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user_info.id:
                return jsonify({'error': 'Email already taken'}), 400
            user_info.email = data['email']

        if 'name' in data:
            user_info.name = data['name']

        db.session.commit()
        return jsonify({'message': 'User updated successfully'})

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user_info = User.query.get(user_id)

        if not user_info:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'id': user_info.id,
            'name': user_info.name,
            'email': user_info.email,
            'role': user_info.role
        })

    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        user_info = User.query.get(user_id)

        if not user_info:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user_info)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200

