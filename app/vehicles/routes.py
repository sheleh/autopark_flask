from app.vehicles.controllers import vehicle_view


def vehicle_module_routes(api):

    api.add_url_rule('/vehicle/', defaults={'vehicle_id': None}, view_func=vehicle_view, methods=['GET', 'POST'])
    api.add_url_rule('/vehicle/<int:vehicle_id>', view_func=vehicle_view, methods=['GET', 'PUT', 'DELETE'])
