from app.companys.controllers import company_view


def company_module_routes(app):
    app.add_url_rule(
        '/api/company/', defaults={'company_id': None}, view_func=company_view, methods=['GET', 'POST', 'PUT']
    )
    app.add_url_rule('/api/company/<int:company_id>', view_func=company_view, methods=['GET', ])
