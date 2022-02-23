from flask import jsonify, request, Response
from flask.views import MethodView
from flask_restful import abort
from app.auth.utils import admin_required, get_current_user
from .models import Company
from flask_jwt_extended import jwt_required
from app.schemas import (
    company_form_schema,
    company_list_form_schema,
    company_update_form_schema
)


class CompanyView(MethodView):
    """Company Api"""

    @jwt_required()
    def get(self, company_id):
        current_user = get_current_user()
        if not current_user.is_staff():
            if company_id:
                company = Company.query.filter_by(id=company_id, owner_id=current_user.id).first_or_404()
                result = company_form_schema.dump(company)
            else:
                company = Company.query.filter_by(owner_id=current_user.id).all()
                result = jsonify({'companies': company_list_form_schema.dump(company)})
        elif current_user.chief_id:
            company = current_user.company
            result = company_form_schema.dump(company)
        else:
            result = {'message': f'User {current_user} is not a member of any company'}
        return result

    @admin_required()
    def post(self, **kwargs):
        current_user = get_current_user()
        data = request.get_json()
        errors = company_form_schema.validate(data)
        if errors:
            abort(Response(f'Incorrect data {errors}', 400))
        name = data.get('name')
        address = data.get('address')
        if Company.find_by_name(name):
            return {'message': f'Company with name {name} already exists'}
        new_company = Company(name=name, address=address, owner_id=current_user.id)
        try:
            new_company.save_to_db()
            return {'message': f'Company {new_company} was created'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    @admin_required()
    def put(self, company_id):
        current_user = get_current_user()
        data = request.get_json()
        errors = company_update_form_schema.validate(data)
        if errors:
            abort(Response(f'Incorrect data {errors}', 400))
        company = Company.query.filter_by(id=company_id, owner_id=current_user.id).first_or_404()
        for key, value in data.items():
            setattr(company, key, value)
        try:
            company.save_to_db()
            return {'message': f'Company {company.name} has been updated'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))


company_view = CompanyView.as_view('company_api')
