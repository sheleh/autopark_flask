from flask import jsonify, request, Response
from flask.views import MethodView
from flask_restful import abort
from sqlalchemy import and_
from app.accounts.models import User
from app.offices.models import Office
from app.companys.models import Company
from app.utils import url_filter
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
    def get(self, office_id):
        current_user = get_current_user()
        if not current_user.is_staff():
            if office_id:
                office = Office.query.filter_by(
                    id=office_id).join(Office.company, aliased=True).filter_by(owner_id=current_user.id).first_or_404()
                result = office_get_form_schema.dump(office)
            else:
                # TODO what if admin have a couple of companies?
                args = request.args
                filters = ['name', 'address', 'country', 'city', 'region']
                query_filters = url_filter(filters, args, Office)
                offices = Office.query.join(
                    Office.company, aliased=True).filter_by(owner_id=current_user.id).filter(and_(*query_filters)).all()
                result = jsonify({'offices': offices_with_company_info_list_form_schema.dump(offices)})
        elif current_user.chief_id:
            if office_id:
                return {'message': 'Administrator permissions required'}, 403
            offices = current_user.company.offices
            result = jsonify({'offices': offices_list_form_schema.dump(offices)})
        else:
            result = {'message': f'User {current_user} is not a member of any company'}
        return result

    @admin_required()
    def post(self, **kwargs):
        current_user = get_current_user()
        data = request.get_json()
        errors = office_form_schema.validate(data)
        if errors:
            response = jsonify({'message': f'Incorrect data {errors}'})
            response.status_code = 400
            return response
        name = data.get('name')
        received_company_id = data.get("company_id")
        company = Company.query.filter_by(owner_id=current_user.id).first_or_404()
        company_id = received_company_id if received_company_id else company.id
        # TODO what if admin sent another admin company_id?
        if Office.check_on_unique_name(name, company_id):
            abort(Response(f'Office with name {name} already exist in {company.name}', 400))
        # TODO Can admin create office to another user company?
        new_office = Office(
            name=name,
            address=data.get('address'),
            country=data.get('country'),
            city=data.get('city'),
            region=data.get('region'),
            company_id=company_id
        )
        try:
            new_office.save_to_db()
            return {'message': f'Office with name {new_office} was created'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    @admin_required()
    def put(self, office_id):
        current_user = get_current_user()
        data = request.get_json()
        errors = offices_update_form_schema.validate(data)
        if errors:
            abort(Response(f'Incorrect data {errors}', 400))
        office = Office.query.filter_by(
            id=office_id).join(Office.company, aliased=True).filter_by(owner_id=current_user.id).first_or_404()
        for key, value in data.items():
            setattr(office, key, value)
        try:
            office.save_to_db()
            return {'message': f'Office {office.name} has been updated'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    @admin_required()
    def delete(self, office_id):
        current_user = get_current_user()
        office = Office.query.filter_by(
            id=office_id).join(Office.company, aliased=True).filter_by(owner_id=current_user.id).first_or_404()
        try:
            office.delete_from_db()
            return {'message': 'Office has been deleted'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))


class UsersAndOfficeRelation(MethodView):
    @admin_required()
    def put(self, office_id, user_id):
        current_user = get_current_user()
        office = Office.query.filter_by(
            id=office_id).join(Office.company, aliased=True).filter_by(owner_id=current_user.id).first_or_404()
        employee = User.query.filter_by(id=user_id, chief_id=current_user.id).first_or_404()
        employee.office_id = office_id
        try:
            office.save_to_db()
            return jsonify(message=f'User {employee.email} has been assigned to {office.name}')
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    @jwt_required()
    def get(self):
        current_user = get_current_user()
        current_user_office = current_user.office
        if not current_user_office:
            return {'message': f'User {current_user} not assigned to any office'}
        return office_get_form_schema.dump(current_user_office)


users_and_offices_relation_view = UsersAndOfficeRelation.as_view('users_and_offices_relation_api')
office_view = OfficeView.as_view('office_api')
