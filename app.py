from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_restful import Api
from flask_migrate import Migrate
from datetime import datetime
import requests
import base64
from config import Config
from database import db, bcrypt, jwt
from resources.products import ProductDisplayResource, ProductResource
from resources.orders import OrderDisplayResource, OrderResource
from resources.users import RegisterResource, UserResource
from dotenv import load_dotenv
load_dotenv()


# Initialize Flask app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from models import Product, Order, OrderItem, User, Cart, Payment

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    api = Api(app)

    migrate = Migrate(app, db)

    # Define home route
    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to the ShopIT API!"})

    # Register API resources
    api.add_resource(ProductDisplayResource, '/products')
    api.add_resource(ProductResource, '/products/<int:id>')
    api.add_resource(OrderDisplayResource, '/orders')
    api.add_resource(OrderResource, '/orders/<int:order_id>')
    api.add_resource(RegisterResource, '/register')
    api.add_resource(UserResource, '/user')

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token})
        return jsonify({'message': 'Invalid credentials'}), 401

    def get_mpesa_token():
        consumer_key = "your_consumer_key"
        consumer_secret = "your_consumer_secret"
        credentials = f"{consumer_key}:{consumer_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {"Authorization": f"Basic {encoded_credentials}"}
        response = requests.get("https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials", headers=headers)

        return response.json().get("access_token", None)

    @app.route('/mpesa-payment', methods=['POST'])
    def mpesa_payment():
        data = request.get_json()
        phone_number = data['phone_number']
        amount = data['amount']
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        business_short_code = '174379'
        passkey = 'your_mpesa_passkey'

        password = base64.b64encode(f"{business_short_code}{passkey}{timestamp}".encode()).decode()
        token = get_mpesa_token()

        if not token:
            return jsonify({"message": "Failed to get M-Pesa token"}), 500

        payload = {
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://your_callback_url.com/mpesa",
            "AccountReference": "ShopIT Payment",
            "TransactionDesc": "Payment for order"
        }

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)
        return response.json()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
