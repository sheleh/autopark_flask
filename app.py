from flask_restful import Api
from app import app
from app import resources
from app.auth.routes import auth_module_routes

from app.resources import (
    user_view,
    company_view,
    profile_view,
    office_view,
    users_and_offices_relation_view,
    vehicle_view
)

api = Api(app)

auth_module_routes(api)

api.add_resource(resources.AdminRegistration, '/admin/registration')

app.add_url_rule('/users/', defaults={'user_id': None}, view_func=user_view, methods=['GET', 'POST'])
app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])

app.add_url_rule('/company/', defaults={'company_id': None}, view_func=company_view, methods=['GET', 'POST'])
app.add_url_rule('/company/<int:company_id>', view_func=company_view, methods=['GET', 'PUT'])

app.add_url_rule('/profile/', view_func=profile_view, methods=['GET', 'PUT'])

app.add_url_rule('/office/', defaults={'office_id': None}, view_func=office_view, methods=['GET', 'POST'])
app.add_url_rule('/office/<int:office_id>', view_func=office_view, methods=['GET', 'PUT', "DELETE"])

app.add_url_rule(
    '/office/<int:office_id>/assign/<int:user_id>', view_func=users_and_offices_relation_view, methods=['PUT']
)
app.add_url_rule('/my_office/', view_func=users_and_offices_relation_view, methods=['GET'])

app.add_url_rule('/vehicle/', defaults={'vehicle_id': None}, view_func=vehicle_view, methods=['GET', 'POST'])
app.add_url_rule('/vehicle/<int:vehicle_id>', view_func=vehicle_view, methods=['GET', 'PUT', 'DELETE'])

app.run(port=5000)
