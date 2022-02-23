from flask_restful import Api
from app import app
from app.accounts.routes import user_module_routes, user_profile_module
from app.auth.routes import auth_module_routes
from app.companys.routes import company_module_routes
from app.offices.routes import office_module_routes
from app.vehicles.routes import vehicle_module_routes

api = Api(app)

auth_module_routes(api)
user_module_routes(app)
company_module_routes(app)
user_profile_module(app)
office_module_routes(app)
vehicle_module_routes(app)

app.run(port=5000)
