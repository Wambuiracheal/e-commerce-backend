from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os

app = Flask(__name__)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], email=data['email'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/user', methods=['PATCH'])
@jwt_required()
def update_user():
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

@app.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    user = get_jwt_identity()
    user_info = User.query.get(user['id'])
    if user_info:
        return jsonify({'id': user_info.id, 'name': user_info.name, 'email': user_info.email, 'role': user_info.role})
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
