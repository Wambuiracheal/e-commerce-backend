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

        if not data["name"].strip():
            return {"message": "Name is required"}, 400

        if User.query.filter_by(email=data["email"]).first():
            return {"message": "User already exists"}, 400
        
        # Validate role
        valid_roles = {"buyer", "seller"}
        role = data.get("role")
        if role not in valid_roles:
            return {"message": "Invalid role. Role must be 'buyer' or 'seller'."}, 400

        # Create new user
        new_user = User(
            name=data["name"].strip(),
            email=data["email"].strip(),
            role=role
        )
        new_user.set_password(data["password"])  # Hash password

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
        if "password" in data and data["password"]:
            user.set_password(data["password"])  # Hash new password

        for key, value in data.items():
            if key != "password" and value.strip():  # Avoid empty updates
                setattr(user, key, value.strip())

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
        return {"message": "User deleted successfully"}, 200
