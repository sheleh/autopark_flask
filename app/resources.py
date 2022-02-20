import pdb
from flask import jsonify, request
from flask.views import MethodView
from flask_restful import Resource

from .auth.helpers import admin_required, get_current_user
from .models import User, RevokedTokenModel, Company, Office
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from .schemas import (
    company_form_schema,
    admin_form_schema,
    users_form_schema,
    single_user_form_schema,
    single_user_update_form_schema,
    user_login_form_schema,
    user_create_form_schema, company_list_form_schema, company_update_form_schema, user_profile_form_schema,
    user_update_profile_form_schema, office_form_schema, offices_list_form_schema, office_get_form_schema,
    offices_update_form_schema, offices_with_company_info_list_form_schema
)


class AdminRegistration(Resource):
    """Admin Registration API"""
    def post(self):
        data = request.get_json()
        errors = admin_form_schema.validate(data)
        if errors:
            return {'message': f'Incorrect data {errors}'}, 400
        email = data.get('email')

        if User.find_by_email(email):
            return {'message': f'User with {email} email already exists'}
        new_user = User(
            email=email,
            password=User.generate_hash(data.get('password')),
            is_stafff=False
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
            return {'message': f"Something went wrong! {str(e)}"}, 400


class UserView(MethodView):
    @jwt_required()
    def get(self, user_id):
        current_user = get_current_user()
        employees = User.query.filter_by(chief_id=current_user.id)
        if user_id:
            employee = employees.first_or_404(user_id)
            result = single_user_form_schema.dump(employee)
        else:
            result = jsonify({'users': users_form_schema.dump(employees)})
        return result

    @jwt_required()
    def post(self, **kwargs):
        current_user = get_current_user()
        company = Company.query.filter_by(owner_id=current_user.id).first()
        data = request.get_json()
        errors = user_create_form_schema.validate(data)
        if errors:
            return {'message': f'Incorrect data {errors}'}, 400
        email = data.get('email')
        if User.find_by_email(email):
            return {'message': f'User with {email} email already exists'}
        new_user = User(
            email=email,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            chief_id=current_user.id,
            password=User.generate_hash(data.get('password')),
            company_id=company.id if company else None
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
            return {'message': f"Something went wrong! {str(e)}"}, 400

    @jwt_required()
    def put(self, user_id):
        current_user = get_current_user()
        data = request.get_json()
        errors = single_user_update_form_schema.validate(data)
        if errors:
            return {'message': f'Incorrect data {errors}'}, 400
        employee = User.query.filter_by(id=user_id, chief_id=current_user.id).first_or_404()
        if data.get('password'):
            data['password'] = User.generate_hash(data.get('password'))
        for key, value in data.items():
            setattr(employee, key, value)
        try:
            employee.save_to_db()
            access_token = create_access_token(identity=data.get('email'))
            refresh_token = create_refresh_token(identity=data.get('email'))
            return {
                'message': 'User has been updated',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except Exception as e:
            return {'message': f"Something went wrong {str(e)}"}, 400

    @jwt_required()
    def delete(self, user_id):
        current_user = get_current_user()
        employee = User.query.filter_by(id=user_id, chief_id=current_user.id).first_or_404()
        try:
            employee.delete_from_db()
            return {'message': 'User has been deleted'}
        except Exception as e:
            return {'message': f"Something went wrong {str(e)}"}, 400


class UserLogin(Resource):
    """User login API"""
    def post(self):
        data = request.get_json()
        errors = user_login_form_schema.validate(data)
        if errors:
            return {'message': f'Incorrect data {errors}'}, 400
        email = data.get('email')
        current_user = User.find_by_email(email)
        # TODO: need to change this condition
        if not current_user:
            return {'message': f'User {email} does not exist'}
        if User.verify_hash(data.get('password'), current_user.password):
            additional_claims = {"id": current_user.id}
            access_token = create_access_token(identity=email, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=email)
            return {
                'message': f'Logged in as {email}',
                'access_token': access_token,
                'refresh': refresh_token,
            }
        else:
            return {'message': "wrong Credentials"}, 403


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except Exception as e:
            return {'message': f"Something went wrong {str(e)}"}, 400


class UserLogoutRefresh(Resource):
    """User Logout Refresh API"""

    @jwt_required
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            pdb.set_trace()
            return {'message': 'Refresh token has been revoked'}
        except Exception as e:
            return {'message': f"Something went wrong {str(e)}"}, 400


class TokenRefresh(Resource):
    """Token Refresh API"""

    @jwt_required
    def post(self):
        # Generating new access token
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


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
    def post(self):
        current_user = get_current_user()
        data = request.get_json()
        errors = company_form_schema.validate(data)
        if errors:
            return {'message': f'Incorrect data {errors}'}, 400
        name = data.get('name')
        address = data.get('address')
        if Company.find_by_name(name):
            return {'message': f'Company with name {name} already exists'}
        new_company = Company(name=name, address=address, owner_id=current_user.id)
        try:
            new_company.save_to_db()
            return {'message': f'Company {new_company} was created'}
        except Exception as e:
            return {'message': f"Something went wrong, exception {str(e)}"}, 400

    @admin_required()
    def put(self, company_id):
        current_user = get_current_user()
        data = request.get_json()
        errors = company_update_form_schema.validate(data)
        if errors:
            return {'message': f'Incorrect data {errors}'}, 400
        company = Company.query.filter_by(id=company_id, owner_id=current_user.id).first_or_404()
        for key, value in data.items():
            setattr(company, key, value)
        try:
            company.save_to_db()
            return {'message': f'Company {company.name} has been updated'}
        except Exception as e:
            return {'message': f"Something went wrong {str(e)}"}, 400


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
            return {'message': f'Incorrect data {errors}'}, 400
        if data.get('password'):
            data['password'] = User.generate_hash(data.get('password'))
        for key, value in data.items():
            setattr(current_user, key, value)
        try:
            current_user.save_to_db()
            return {'message': f'User {current_user} has been updated'}
        except Exception as e:
            return {'message': f"Something went wrong {str(e)}"}, 400


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
                offices = Office.query.join(Office.company, aliased=True).filter_by(owner_id=current_user.id).all()
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
            return {'message': f'Incorrect data {errors}'}, 400
        name = data.get('name')
        received_company_id = data.get("company_id")
        company = Company.query.filter_by(owner_id=current_user.id).first_or_404()
        company_id = received_company_id if received_company_id else company.id
        if Office.check_on_unique_name(name, company_id):
            return {'message': f'Office with name {name} already exist in {company.name}'}
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
            return {'message': f"Something went wrong, exception {str(e)}"}, 400

    @admin_required()
    def put(self, office_id):
        current_user = get_current_user()
        data = request.get_json()
        errors = offices_update_form_schema.validate(data)
        if errors:
            return {'message': f'Incorrect data {errors}'}, 400
        office = Office.query.filter_by(
            id=office_id).join(Office.company, aliased=True).filter_by(owner_id=current_user.id).first_or_404()
        for key, value in data.items():
            setattr(office, key, value)
        try:
            office.save_to_db()
            return {'message': f'Office {office.name} has been updated'}
        except Exception as e:
            return {'message': f"Something went wrong {str(e)}"}, 400

    @admin_required()
    def delete(self, office_id):
        current_user = get_current_user()
        office = Office.query.filter_by(
            id=office_id).join(Office.company, aliased=True).filter_by(owner_id=current_user.id).first_or_404()
        try:
            office.delete_from_db()
            return {'message': 'Office has been deleted'}
        except Exception as e:
            return {'message': f"Something went wrong {str(e)}"}, 400


profile_view = ProfileView.as_view('profile_api')
user_view = UserView.as_view('user_api')
company_view = CompanyView.as_view('company_api')
office_view = OfficeView.as_view('office_view')
