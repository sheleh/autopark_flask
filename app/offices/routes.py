from app.offices.controllers import office_view, users_and_offices_relation_view


def office_module_routes(api):

    api.add_url_rule('/office/', defaults={'office_id': None}, view_func=office_view, methods=['GET', 'POST'])
    api.add_url_rule('/office/<int:office_id>', view_func=office_view, methods=['GET', 'PUT', "DELETE"])
    api.add_url_rule(
        '/office/<int:office_id>/assign/<int:user_id>', view_func=users_and_offices_relation_view, methods=['PUT']
    )
    api.add_url_rule('/my_office/', view_func=users_and_offices_relation_view, methods=['GET'])
