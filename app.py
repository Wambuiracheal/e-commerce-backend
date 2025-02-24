from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from models import db
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopIT.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

if __name__ == '__main__':
    app.run(debug=True)

