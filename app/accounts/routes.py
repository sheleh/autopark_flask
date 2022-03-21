from app.accounts.controllers import user_view, profile_view, admin_registration_view


def user_module_routes(api):

    api.add_url_rule('/api/users/', defaults={'user_id': None}, view_func=user_view, methods=['GET', 'POST'])
    api.add_url_rule('/api/users/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])
    api.add_url_rule('/api/admin/registration/', view_func=admin_registration_view, methods=['POST'])


def user_profile_module(api):
    api.add_url_rule('/api/profile/', view_func=profile_view, methods=['GET', 'PUT'])
