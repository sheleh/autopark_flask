from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

import app
from app.accounts.routes import user_module_routes, user_profile_module
from app.auth.routes import auth_module_routes
from app.companys.routes import company_module_routes
from app.offices.routes import office_module_routes
from app.vehicles.routes import vehicle_module_routes
from app.schemas import ma
from app.database.models import User, RevokedTokenModel
from config import DevelopmentConfig, TestingConfig

jwt_obj = JWTManager()
api_obj = Api()
db_obj = SQLAlchemy()
migrate_obj = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    from app.database.models import db
    db.init_app(app)
    auth_module_routes(api=api_obj)
    initialize_extensions(app)
    initialize_routes(app)

    return app


def initialize_extensions(app):

    ma.init_app(app)
    jwt_obj.init_app(app)
    api_obj.init_app(app)
    db_obj.init_app(app)
    migrate_obj.init_app(app, db)


def initialize_routes(app):
    user_module_routes(app)
    company_module_routes(app)
    user_profile_module(app)
    office_module_routes(app)
    vehicle_module_routes(app)


@jwt_obj.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


from app.database.models import *
