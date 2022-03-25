from flask.views import MethodView
from app.auth.utils import admin_required, get_current_user
from app.database.models import Company
from flask_jwt_extended import jwt_required
from app.schemas import (
    company_form_schema,
    company_update_form_schema
)
from app.utils import validate_request_data


class CompanyView(MethodView):
    """Company Api"""
    @jwt_required()
    def __init__(self):
        self.current_user = get_current_user()

    def get(self):
        company = self.current_user.company
        return company_form_schema.dump(company)

    @admin_required()
    def post(self):
        data = validate_request_data(company_form_schema)
        name = data.get('name')
        if Company.find_by_name(name):
            return {'message': f'Company with name {name} already exists'}, 400
        if Company.check_by_owner(self.current_user.id):
            return {'message': f'User {self.current_user.email} has already created a company'}, 400
        new_company = Company(name=name, address=data.get('address'), owner_id=self.current_user.id)
        new_company.save_to_db()
        self.current_user.company_id = new_company.id
        self.current_user.save_to_db()
        return {'message': f'Company {new_company} was created'}, 201

    @admin_required()
    def put(self):
        data = validate_request_data(company_update_form_schema)
        company = Company.query.filter_by(id=self.current_user.company_id, owner_id=self.current_user.id).first_or_404()
        for key, value in data.items():
            setattr(company, key, value)
        company.save_to_db()
        return {'message': f'Company {company.name} has been updated'}, 200


company_view = CompanyView.as_view('company_api')
