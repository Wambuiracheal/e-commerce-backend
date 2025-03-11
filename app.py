import os
import json
import requests
import base64
import datetime
from datetime import timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS,cross_origin
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from models import db, OrderItem, Cart, User, Product
from resources.shop import UserResource ,RegisterResource, LoginResource, ProductDisplayResource, ProductResource, OrderDisplayResource, OrderResource, BuyerDisplayResource, BuyerResource

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopit.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'bc9f3a4897ef90fc6c27f17ee1905a2f'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
    
    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    Bcrypt(app)
    JWTManager(app)
    
    with app.app_context():
        db.create_all()
    
    # Register API routes
    api.add_resource(ProductDisplayResource, '/products')
    api.add_resource(ProductResource, '/products/<int:id>')
    api.add_resource(BuyerDisplayResource, '/buyer')
    api.add_resource(BuyerResource, '/buyer/<int:id>')
    api.add_resource(OrderDisplayResource, '/orders')
    api.add_resource(OrderResource, '/orders/<int:id>')
    api.add_resource(RegisterResource, '/register')
    api.add_resource(UserResource, '/user')
    api.add_resource(LoginResource, '/login')
    
    @app.route('/')
    def home():
        return '<h1>Welcome to ShopIT</h1><p>Where quality meets affordability</p>'
    
    # Order Items Routes
    @app.route('/order_items', methods=['GET', 'POST'])
    def order_items():
        if request.method == 'GET':
            items = OrderItem.query.all()
            return jsonify([item.to_dict() for item in items])
        elif request.method == 'POST':
            data = request.json
            new_item = OrderItem(**data)
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'message': 'Order item added successfully', 'id': new_item.id}), 201
    
    @app.route('/order_items/<int:item_id>', methods=['GET'])
    def get_order_item(item_id):
        item = OrderItem.query.get(item_id)
        if not item:
            return jsonify({'error': 'Order item not found'}), 404
        return jsonify(item.to_dict())
    
    # Cart Routes
    @app.route('/cart', methods=['GET', 'POST'])
    def cart():
        if request.method == 'GET':
            return jsonify([item.to_dict() for item in Cart.query.all()]), 200
        elif request.method == 'POST':
            data = request.get_json()
            new_cart_item = Cart(**data)
            db.session.add(new_cart_item)
            db.session.commit()
            return jsonify(new_cart_item.to_dict()), 201
    
    @app.route('/cart/<int:cart_id>', methods=['DELETE'])
    def delete_cart_item(cart_id):
        cart_item = Cart.query.get(cart_id)
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Cart item removed'}), 200
    
    # MPESA Payment Integration
    consumer_key = "1dod7XxWDUZ47l5haEteatUPA9gAQab2qndGq1i99vdMRgrw"
    consumer_secret = "v7NRdg8ImXtVejf7PHOWI8BUrl3LGBjnZHNDJeyrJKaAn95R08AZ6sAoKGjm18rF"
    shortcode = "174379"
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    callback_url = "https://4ab0-105-163-1-181.ngrok-free.app/mpesa/callback"
    
    # print("M-Pesa Response:", response.status_code, response.text)


    @app.route('/mpesa/pay', methods = ['POST'])
    @cross_origin()
    def mpesa_pay():
        phone_number = request.json.get('phone_number')
        amount = request.json.get('amount')

        access_token = get_access_token()
        if not access_token:
            return jsonify({'error' : 'Failed to get mpesa access token!'}), 500

        headers = {
            'Authorization' : f'Bearer {access_token}',
            'Content-Type' : 'application/json'
        }

        timestamp = get_timestamp()
        print(f"Generated Timestamp: {timestamp}")
        password = generate_password(shortcode, passkey, timestamp)

        payload = {
            "BusinessShortCode" : shortcode,
            "Password" : password,
            "Timestamp" : timestamp,
            "TransactionType" : "CustomerPayBillOnline",
            "Amount" : amount,
            "PartyA" : phone_number,
            "PartyB" : shortcode,
            "PhoneNumber" : phone_number,
            "CallBackURL" : callback_url,
            "AccountReference" : "12345678",
            "TransactionDesc" : "Payment for abc"
        }

        stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        response = requests.post(stk_push_url, json=payload, headers=headers)

        if response.status_code == 200:
            return jsonify({'message' : 'STK push initiated successfully', "data": response.json()}), 200
        else:
            return jsonify({'error' : 'Failed to initiate STK push', 'data': response.json()}), 500

    @app.route('/mpesa/callback', methods = ['POST'])
    def mpesa_callback():
        data = request.get_json()

        with open('mpesa_callback.log', 'a') as log_file:
            log_file.write(json.dumps(data, indent=4) + '\n\n')

        try:
            result_code = data['Body']['stkCallback']['ResultCode']
            result_desc = data['Body']['stkCallback']['ResultDesc']

            if result_code == 0:
                callback_metadata = data['Body']['stkCallback']['CallbackMetadata']['Item']
                amount = next(item['Value'] for item in callback_metadata if item['Name'] == 'Amount')
                mpesa_receipt_number = next(item['Value'] for item in callback_metadata if item['Name'] == 'MpesaReceiptNumber')
                phone_number = next(item['Value'] for item in callback_metadata if item['Name'] == 'PhoneNumber')

                payment_status = {
                    'status' : 'success',
                    'amount' : amount,
                    'receipt' : mpesa_receipt_number,
                    'phone' : phone_number,
                    'message' : 'Payment received successfully!'
                }

            else:
                payment_status = {
                    'status' : 'Failed',
                    'message' : result_desc
                }
            return jsonify ({'message' : 'Callback received!'}), 200

        except KeyError:
            return jsonify ({'error' : 'invalid callback data'}), 400

    def get_access_token():
        url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        response = requests.get(url, auth=(consumer_key, consumer_secret))
        return response.json().get('access_token') if response.status_code == 200 else None

    def generate_password(shortcode, passkey, timestamp):
        data_to_encode = f'{shortcode}{passkey}{timestamp}'
        return base64.b64encode(data_to_encode.encode()).decode('utf-8')

    def get_timestamp():
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    # timestamp = get_timestamp()
    # print(f"Timestamp: {timestamp}")
    
    return app
app = create_app()
if __name__ == '__main__':
   
    app.run(debug=True)
