from flask import request, jsonify
from flask_restful import Resource
from models import Order,db
from flask_jwt_extended import jwt_required, get_jwt_identity

class OrderDisplayResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()  # Get the logged-in user ID
        orders = Order.query.filter_by(user_id=user_id).all()
        return [order.to_dict() for order in orders], 200

class OrderResource(Resource):
    @jwt_required()
    def get(self, order_id):
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()

        if not order:
            return {"message": "Order not found or unauthorized"}, 404

        return order.to_dict(), 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        new_order = Order(**data, user_id=user_id)  # Assign order to the logged-in user

        db.session.add(new_order)
        db.session.commit()
        return new_order.to_dict(), 201

    @jwt_required()
    def put(self, order_id):
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()

        if not order:
            return {"message": "Order not found or unauthorized"}, 404

        data = request.get_json()
        for key, value in data.items():
            setattr(order, key, value)
        
        db.session.commit()
        return order.to_dict(), 200

    @jwt_required()
    def delete(self, order_id):
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()

        if not order:
            return {"message": "Order not found or unauthorized"}, 404

        db.session.delete(order)
        db.session.commit()
        return {"message": "Order deleted"}, 200