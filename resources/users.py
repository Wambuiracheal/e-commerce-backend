from flask import request, jsonify
from flask_restful import Resource
from database import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()

        # Validate required fields
        required_fields = {"name", "email", "password", "role"}
        if not data or not required_fields.issubset(data.keys()):
            return {"message": "Missing required fields"}, 400

        if not data["name"]:
            return {"message": "Name is required"}, 400

        # Check if user already exists
        if User.query.filter_by(email=data["email"]).first():
            return {"message": "User already exists"}, 400
        
        # Validate role
        valid_roles = {"buyer", "seller"}
        role = data.get("role")

        if role not in valid_roles:
            return {"message": "Invalid role. Role must be 'buyer' or 'seller'."}, 400

        hashed_password = generate_password_hash(data["password"]) 

        # Create new user
        new_user = User(
            name=data["name"], 
            email=data["email"], 
            password=hashed_password, 
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201


class UserResource(Resource):
    @jwt_required() 
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return jsonify(user.to_dict()), 200

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        data = request.get_json()
        if "password" in data:
            data["password"] = generate_password_hash(data["password"], method="pbkdf2:sha256")

        for key, value in data.items():
            setattr(user, key, value)

        db.session.commit()
        return user.to_dict(), 200

    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200
