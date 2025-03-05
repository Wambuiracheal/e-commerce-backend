import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///shopit.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret")
    CORS_HEADERS = 'Content-Type'

    # M-Pesa API Credentials
    MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY", "default_consumer_key")
    MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET", "default_consumer_secret")
    MPESA_SHORTCODE = "174379"
    MPESA_PASSKEY = os.getenv("MPESA_PASSKEY", "default_mpesa_passkey")
    CALLBACK_URL = os.getenv("CALLBACK_URL", "https://yourdomain.com/mpesa/callback")
