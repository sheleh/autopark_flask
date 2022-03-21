from app.vehicles.controllers import vehicle_view, worker_vehicles_view


def vehicle_module_routes(api):

    api.add_url_rule('/api/vehicles/', defaults={'vehicle_id': None}, view_func=vehicle_view, methods=['GET', 'POST'])
    api.add_url_rule('/api/vehicles/<int:vehicle_id>', view_func=vehicle_view, methods=['GET', 'PUT', 'DELETE'])
    api.add_url_rule('/api/my_vehicles/', view_func=worker_vehicles_view, methods=['GET'])
