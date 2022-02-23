from flask import jsonify, request, Response
from flask.views import MethodView
from flask_restful import abort
from app.accounts.models import User
from app.offices.models import Office
from app.vehicles.models import Vehicle
from app.companys.models import Company
from app.auth.utils import admin_required, get_current_user
from flask_jwt_extended import jwt_required
from app.schemas import (
    vehicle_create_form_schema,
    vehicle_list_form_schema,
    vehicle_update_form_schema,
    vehicle_staff_form_schema
)


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


vehicle_view = VehicleView.as_view('vehicle_view_api')
