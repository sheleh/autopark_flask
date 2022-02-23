from app.companys.controllers import company_view


def company_module_routes(api):

    api.add_url_rule('/company/', defaults={'company_id': None}, view_func=company_view, methods=['GET', 'POST'])
    api.add_url_rule('/company/<int:company_id>', view_func=company_view, methods=['GET', 'PUT'])
