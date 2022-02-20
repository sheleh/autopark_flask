from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig
from flask_marshmallow import Marshmallow
app = Flask(__name__)


app.config.from_object(DevelopmentConfig)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
from app import routes, models

migrate = Migrate(app, db)

