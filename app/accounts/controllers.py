from flask import jsonify, request, Response
from flask.views import MethodView
from flask_restful import Resource, abort
from sqlalchemy import and_
from app.utils import url_filter
from app.companys.models import Company
from app.auth.utils import admin_required, get_current_user
from .models import User
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


class AdminRegistration(Resource):
    """Admin Registration API"""
    def post(self):
        data = request.get_json()
        errors = admin_form_schema.validate(data)
        if errors:
            abort(Response(f'Incorrect data {errors}', 400))
        email = data.get('email')

        if User.find_by_email(email):
            return {'message': f'User with {email} email already exists'}
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
        try:
            new_user.save_to_db()
            return {
                'message': f'User {email} was created',
            }
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))


class UserView(MethodView):

    @admin_required()
    def get(self, user_id):
        args = request.args
        filters = ['last_name', 'first_name', 'email']
        current_user = get_current_user()
        query_filters = url_filter(filters, args, User)

        employees = User.query.filter_by(chief_id=current_user.id).filter(and_(*query_filters))
        if user_id:
            employee = employees.filter_by(id=user_id).first_or_404()
            result = single_user_form_schema.dump(employee)
        else:
            result = jsonify({'users': users_form_schema.dump(employees)})
        return result

    @admin_required()
    def post(self, **kwargs):
        current_user = get_current_user()
        data = request.get_json()
        errors = user_create_form_schema.validate(data)
        if errors:
            abort(Response(f'Incorrect data {errors}', 400))
        email = data.get('email')
        company = Company.query.filter_by(owner_id=current_user.id).first()
        if User.find_by_email(email):
            return {'message': f'User with {email} email already exists'}
        new_user = User(
            email=email,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            is_stafff=True,
            chief_id=current_user.id,
            password=User.generate_hash(data.get('password')),
            company_id=company.id if company else None,
            office_id=None
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            return {
                'message': f'User {email} was created',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    @jwt_required()
    def put(self, user_id):
        current_user = get_current_user()
        data = request.get_json()
        errors = single_user_update_form_schema.validate(data)
        if errors:
            abort(Response(f'Incorrect data {errors}', 400))
        employee = User.query.filter_by(id=user_id, chief_id=current_user.id).first_or_404()
        if data.get('password'):
            data['password'] = User.generate_hash(data.get('password'))
        for key, value in data.items():
            setattr(employee, key, value)
        try:
            employee.save_to_db()
            return {
                'message': 'User has been updated',
            }
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    @jwt_required()
    def delete(self, user_id):
        current_user = get_current_user()
        employee = User.query.filter_by(id=user_id, chief_id=current_user.id).first_or_404()
        try:
            employee.delete_from_db()
            return {'message': 'User has been deleted'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))


class ProfileView(MethodView):

    @jwt_required()
    def get(self):
        current_user = get_current_user()
        result = user_profile_form_schema.dump(current_user)
        return result

    @jwt_required()
    def put(self):
        current_user = get_current_user()
        data = request.get_json()
        errors = user_update_profile_form_schema.validate(data)
        if errors:
            abort(Response(f'Incorrect data {errors}', 400))
        if data.get('password'):
            data['password'] = User.generate_hash(data.get('password'))
        for key, value in data.items():
            setattr(current_user, key, value)
        try:
            current_user.save_to_db()
            return {'message': f'User {current_user} has been updated'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))


profile_view = ProfileView.as_view('profile_api')
user_view = UserView.as_view('user_api')
