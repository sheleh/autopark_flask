from flask import jsonify, request, Response
from flask.views import MethodView
from flask_restful import Resource, abort
from sqlalchemy import and_
from .utils import url_filter
from .auth.utils import admin_required, get_current_user
from .models import User, Company, Office, Vehicle
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
)
from .schemas import (
    company_form_schema,
    admin_form_schema,
    users_form_schema,
    single_user_form_schema,
    single_user_update_form_schema,
    user_create_form_schema, company_list_form_schema, company_update_form_schema, user_profile_form_schema,
    user_update_profile_form_schema, office_form_schema, offices_list_form_schema, office_get_form_schema,
    offices_update_form_schema, offices_with_company_info_list_form_schema, vehicle_create_form_schema,
    vehicle_list_form_schema, vehicle_update_form_schema, vehicle_staff_form_schema
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
            # access_token = create_access_token(identity=email)
            # refresh_token = create_refresh_token(identity=email)
            return {
                'message': f'User {email} was created',
                # 'access_token': access_token,
                # 'refresh_token': refresh_token
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


class VehicleView(MethodView):

    @jwt_required()
    def get(self, vehicle_id):
        current_user = get_current_user()
        if not current_user.is_staff():
            if vehicle_id:
                vehicle = Vehicle.query.join(Company, aliased=True).filter(Vehicle.id == vehicle_id).filter(
                    Company.owner_id == current_user.id).first_or_404()
                result = vehicle_create_form_schema.dump(vehicle)
            else:
                # TODO what if admin have a couple of companies?
                args = request.args
                filters = ['office_id', 'driver_id']
                checked_arg = {
                    key: value if key in filters and value.isdigit() else
                    abort(Response(f'Incorrect filter', 400)) for key, value in args.items()
                }
                args_office = checked_arg.get('office_id')
                args_driver = checked_arg.get('driver_id')
                if args_office and args_driver:
                    vehicles = Vehicle.query.filter_by(
                        office_id=args_office).join(Vehicle.driver).filter_by(
                        id=args_driver).join(Vehicle.company).filter_by(
                        owner_id=current_user.id).all()
                    result = jsonify({'vehicles': vehicle_list_form_schema.dump(vehicles)})
                elif args_driver:
                    driver = User.query.filter_by(id=args_driver, chief_id=current_user.id).first_or_404()
                    result = jsonify({'vehicles': vehicle_list_form_schema.dump(driver.vehicle)})
                elif args_office:
                    office = Office.query.filter_by(
                        id=args_office).join(Office.company, aliased=True).filter_by(
                        owner_id=current_user.id).first_or_404()
                    result = jsonify({'vehicles': vehicle_list_form_schema.dump(office.vehicles)})
                else:
                    company = Company.query.filter_by(owner_id=current_user.id).first_or_404()
                    result = jsonify({'vehicles': vehicle_list_form_schema.dump(company.vehicles)})

        elif current_user.chief_id:
            if vehicle_id:
                return {'message': 'Administrator permissions required'}, 403
            vehicles = current_user.vehicle
            result = jsonify({'vehicle': vehicle_staff_form_schema.dump(vehicles)})
        else:
            result = {'message': f'User {current_user} is not a member of any company'}, 403
        return result

    @admin_required()
    def post(self, **kwargs):
        current_user = get_current_user()
        company = Company.query.filter_by(owner_id=current_user.id).first()
        data = request.get_json()
        errors = vehicle_create_form_schema.validate(data)
        if errors:
            abort(Response(f'Incorrect data {errors}', 400))

        received_company_id = data.get("company_id")
        license_plate = data.get('license_plate')
        office_id = data.get('office_id')
        driver_id = data.get('driver_id')
        if Vehicle.check_on_unique_license_plate(license_plate):
            return {'message': f'Vehicle with license plate {license_plate} already exists'}
        if office_id and not company.check_office_exists(office_id):
            abort(Response(f'Office with id = {office_id} not exists in company', 400))
        driver = User.query.filter_by(id=driver_id, office_id=office_id).first()
        new_vehicle = Vehicle(
            license_plate=license_plate,
            name=data.get('name'),
            model=data.get('model'),
            year_of_manufacture=data.get('year_of_manufacture'),
            company_id=received_company_id if received_company_id else company.id,
            office_id=office_id
        )
        try:
            if driver:
                new_vehicle.driver.append(driver)
            new_vehicle.save_to_db()
            return {'message': f'Vehicle {new_vehicle.license_plate} {new_vehicle.name} was created'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    @admin_required()
    def put(self, vehicle_id):
        current_user = get_current_user()
        data = request.get_json()
        errors = vehicle_update_form_schema.validate(data)
        if errors:
            abort(Response(f'Incorrect data {errors}', 400))
        office_id = data.get('office_id')
        driver_id = data.get('driver_id')
        company = Company.query.filter_by(owner_id=current_user.id).first()
        if office_id and not company.check_office_exists(office_id):
            abort(Response(f'Office with id = {office_id} not exists in company', 400))
        driver = User.query.filter_by(id=driver_id, office_id=office_id).first()
        if not driver:
            abort(Response(f'You can not assign driver to this vehicle', 400))
        vehicle = Vehicle.query.join(Company, aliased=True).filter(Vehicle.id == vehicle_id).filter(
            Company.owner_id == current_user.id).first_or_404()
        for key, value in data.items():
            setattr(vehicle, key, value)
        try:
            if driver:
                vehicle.driver.append(driver)
            vehicle.save_to_db()
            return {'message': f'Vehicle {vehicle.name} {vehicle.license_plate} has been updated'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))

    @admin_required()
    def delete(self, vehicle_id):
        current_user = get_current_user()
        vehicle = Vehicle.query.join(Company, aliased=True).filter(Vehicle.id == vehicle_id).filter(
            Company.owner_id == current_user.id).first_or_404()
        try:
            vehicle.delete_from_db()
            return {'message': f'Vehicle {vehicle.name} {vehicle.license_plate} has been deleted'}
        except Exception as e:
            abort(Response(f'Something went wrong! {e}', 400))


profile_view = ProfileView.as_view('profile_api')
user_view = UserView.as_view('user_api')
company_view = CompanyView.as_view('company_api')
office_view = OfficeView.as_view('office_api')
users_and_offices_relation_view = UsersAndOfficeRelation.as_view('users_and_offices_relation_api')
vehicle_view = VehicleView.as_view('vehicle_view_api')