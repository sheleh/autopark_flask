from flask_restful import Api
from app import app
from app.models import db
from app import models, resources
from app.resources import user_view, company_view, profile_view, office_view

api = Api(app)


# Generating tables before first request is fetched
@app.before_first_request
def create_tables():
    db.create_all()


# Checking that token is in blacklist or not
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


# api Endpoints
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')

api.add_resource(resources.AdminRegistration, '/admin/registration')

app.add_url_rule('/users/', defaults={'user_id': None}, view_func=user_view, methods=['GET', 'POST'])
app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])

app.add_url_rule('/company/', defaults={'company_id': None}, view_func=company_view, methods=['GET', 'POST'])
app.add_url_rule('/company/<int:company_id>', view_func=company_view, methods=['GET', 'PUT'])

app.add_url_rule('/profile/', view_func=profile_view, methods=['GET', 'PUT'])

app.add_url_rule('/office/', defaults={'office_id': None}, view_func=office_view, methods=['GET', 'POST'])
app.add_url_rule('/office/<int:office_id>', view_func=office_view, methods=['GET', 'PUT'])

# #api.add_resource(resources.UserRegistration, '/user/registration')
# api.add_resource(resources.UserRegistration, '/users', endpoint="UserRegistration",
#                  resource_class_kwargs={"get_request_allowed": True, "post_request_allowed": True})
# api.add_resource(resources.UserRegistration, '/users/get', endpoint="UserRegistration_get",
#                  resource_class_kwargs={"get_request_allowed": True})

#api.add_resource(resources.AllUsers, '/users')

app.run(port=5000)
