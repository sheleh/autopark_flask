from flask import jsonify, request, Response
from flask.views import MethodView
from flask_restful import Resource, abort
from sqlalchemy import and_
from app.utils import url_filter, validate_request_data
from app.database.models import Company, User
from app.auth.utils import admin_required, get_current_user
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
)
from app.schemas import (
    admin_form_schema,
    users_form_schema,
    single_user_form_schema,
    single_user_update_form_schema,
    user_create_form_schema, user_profile_form_schema,
    user_update_profile_form_schema,
)


class AdminRegistration(MethodView):
    """Admin Registration API"""
    def post(self):
        data = validate_request_data(admin_form_schema)
        email = data.get('email')
        if User.find_by_email(email):
            return {'message': f'User with {email} email already exists'}, 400
        new_user = User(
            email=email,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            password=User.generate_hash(data.get('password')),
            is_stafff=False,
            company_id=None,
            office_id=None,
            chief_id=None,
        )
        new_user.save_to_db()
        return {'message': f'User {email} was created'}, 201


class AdminUserView(MethodView):
    @jwt_required()
    def __init__(self):
        self.current_user = get_current_user()

    @admin_required()
    def get(self, user_id):
        args = request.args
        filters = ['last_name', 'first_name', 'email']
        query_filters = url_filter(filters, args, User)
        employees = User.query.filter_by(chief_id=self.current_user.id).filter(and_(True, *query_filters))
        if user_id:
            employee = employees.filter_by(id=user_id).first_or_404()
            result = single_user_form_schema.dump(employee)
        else:
            result = jsonify({'users': users_form_schema.dump(employees)})
        return result

    @admin_required()
    def post(self, **kwargs):
        data = validate_request_data(user_create_form_schema)
        email = data.get('email')
        company = Company.query.filter_by(owner_id=self.current_user.id).first()
        if User.find_by_email(email):
            abort(Response({ f'User with {email} email already exists'}, 400))
        new_user = User(
            email=email,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            is_stafff=True,
            chief_id=self.current_user.id,
            password=User.generate_hash(data.get('password')),
            company_id=company.id if company else None,
            office_id=None
        )

        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        new_user.save_to_db()
        return {
            'message': f'User {email} was created',
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 201

    @admin_required()
    def put(self, user_id):
        data = validate_request_data(single_user_update_form_schema)
        employee = User.query.filter_by(id=user_id, chief_id=self.current_user.id).first_or_404()
        if data.get('password'):
            data['password'] = User.generate_hash(data.get('password'))
        for key, value in data.items():
            setattr(employee, key, value)
        employee.save_to_db()
        return {'message': 'User has been updated'}

    @admin_required()
    def delete(self, user_id):
        employee = User.query.filter_by(id=user_id, chief_id=self.current_user.id).first_or_404()
        employee.delete_from_db()
        return {'message': 'User has been deleted'}


class ProfileView(MethodView):
    @jwt_required()
    def __init__(self):
        self.current_user = get_current_user()

    def get(self):
        result = user_profile_form_schema.dump(self.current_user)
        return result

    def put(self):
        data = validate_request_data(user_update_profile_form_schema)
        if data.get('password'):
            data['password'] = User.generate_hash(data.get('password'))
        for key, value in data.items():
            setattr(self.current_user, key, value)
        self.current_user.save_to_db()
        return {'message': f'User {self.current_user} has been updated'}


profile_view = ProfileView.as_view('profile_api')
user_view = AdminUserView.as_view('user_api')
admin_registration_view = AdminRegistration.as_view('admin_registration_view_api')
