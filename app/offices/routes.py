from app.offices.controllers import office_view, users_and_offices_relation_view, my_office_view


def office_module_routes(api):

    api.add_url_rule('/api/offices/', defaults={'office_id': None}, view_func=office_view, methods=['GET', 'POST'])
    api.add_url_rule('/api/offices/<int:office_id>', view_func=office_view, methods=['GET', 'PUT', "DELETE"])
    api.add_url_rule(
        '/api/offices/<int:office_id>/assign/<int:user_id>', view_func=users_and_offices_relation_view, methods=['PUT']
    )
    api.add_url_rule('/api/my_office/', view_func=my_office_view, methods=['GET'])
