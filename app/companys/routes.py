from app.companys.controllers import company_view


def company_module_routes(app):
    app.add_url_rule(
        '/api/company/', view_func=company_view, methods=['GET', 'POST', 'PUT']
    )
