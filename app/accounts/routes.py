from app.accounts.controllers import user_view, AdminRegistration, profile_view


def user_module_routes(api):

    api.add_url_rule('/users/', defaults={'user_id': None}, view_func=user_view, methods=['GET', 'POST'])
    api.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])


def admin_registration_module(api):
    api.add_resource(AdminRegistration, '/admin/registration')


def user_profile_module(api):
    api.add_url_rule('/profile/', view_func=profile_view, methods=['GET', 'PUT'])
