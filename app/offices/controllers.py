from flask import jsonify, request, Response
from flask.views import MethodView
from flask_restful import abort
from sqlalchemy import and_
from app.database.models import User, Office, Company
from app.utils import url_filter, validate_request_data
from app.auth.utils import admin_required, get_current_user

from flask_jwt_extended import jwt_required
from app.schemas import (
    office_form_schema,
    offices_list_form_schema,
    office_get_form_schema,
    offices_update_form_schema,
    offices_with_company_info_list_form_schema
)


class OfficeView(MethodView):
    @jwt_required()
    def __init__(self):
        self.current_user = get_current_user()

    @jwt_required()
    def get(self, office_id):
        if self.current_user.is_stafff:
            if office_id:
                return {'message': 'Administrator permissions required'}, 403
            offices = self.current_user.company.offices
            result = jsonify({'offices': offices_list_form_schema.dump(offices)})
        else:
            if office_id:
                office = Office.query.filter_by(
                    id=office_id).join(Office.company, aliased=True).filter_by(
                    owner_id=self.current_user.id).first_or_404()
                result = office_get_form_schema.dump(office)
            else:
                args = request.args
                filters = ['name', 'address', 'country', 'city', 'region']
                query_filters = url_filter(filters, args, Office)
                offices = Office.query.join(
                    Office.company, aliased=True).filter_by(
                    owner_id=self.current_user.id).filter(and_(True, *query_filters)).all()
                result = jsonify({'offices': offices_with_company_info_list_form_schema.dump(offices)})
        return result

    @admin_required()
    def post(self, **kwargs):
        data = validate_request_data(office_form_schema)
        name = data.get('name')
        company = Company.query.filter_by(owner_id=self.current_user.id).first_or_404()
        if Office.check_on_unique_name(name, company.id):
            abort(Response(f'Office with name {name} already exist in {company.name}', 400))
        new_office = Office(
            name=name,
            address=data.get('address'),
            country=data.get('country'),
            city=data.get('city'),
            region=data.get('region'),
            company_id=company.id
        )
        new_office.save_to_db()
        return {'message': f'Office with name {new_office} was created'}

    @admin_required()
    def put(self, office_id):
        data = validate_request_data(offices_update_form_schema)
        office = Office.query.filter_by(
            id=office_id).join(Office.company, aliased=True).filter_by(owner_id=self.current_user.id).first_or_404()
        for key, value in data.items():
            setattr(office, key, value)
        office.save_to_db()
        return {'message': f'Office {office.name} has been updated'}

    @admin_required()
    def delete(self, office_id):
        office = Office.query.filter_by(
            id=office_id).join(Office.company, aliased=True).filter_by(owner_id=self.current_user.id).first_or_404()

        office.delete_from_db()
        return {'message': 'Office has been deleted'}


class UsersAndOfficeRelation(MethodView):
    @jwt_required()
    def __init__(self):
        self.current_user = get_current_user()

    @admin_required()
    def put(self, office_id, user_id):
        office = Office.query.filter_by(
            id=office_id).join(Office.company, aliased=True).filter_by(owner_id=self.current_user.id).first_or_404()
        employee = User.query.filter_by(id=user_id, chief_id=self.current_user.id).first_or_404()
        employee.office_id = office_id
        office.save_to_db()
        return jsonify(message=f'User {employee.email} has been assigned to {office.name}')

    def get(self):
        current_user_office = self.current_user.office
        if not current_user_office:
            return {'message': f'User {self.current_user} not assigned to any office'}
        return office_get_form_schema.dump(current_user_office)


users_and_offices_relation_view = UsersAndOfficeRelation.as_view('users_and_offices_relation_api')
office_view = OfficeView.as_view('office_api')
