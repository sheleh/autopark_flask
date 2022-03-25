from flask import jsonify, request, Response
from flask.views import MethodView
from flask_restful import abort
from app.database.models import User, Office, Vehicle, Company
from app.auth.utils import admin_required, get_current_user
from flask_jwt_extended import jwt_required
from app.schemas import (
    vehicle_create_form_schema,
    vehicle_list_form_schema,
    vehicle_update_form_schema,
    vehicle_staff_form_schema,
    vehicle_retrieve_form_schema
)
from app.utils import validate_request_data


class MyVehiclesView(MethodView):
    @jwt_required()
    def get(self):
        current_user = get_current_user()
        vehicles = current_user.vehicle
        return jsonify({'vehicles': vehicle_staff_form_schema.dump(vehicles)})


class AdminVehicleView(MethodView):
    @admin_required()
    def __init__(self):
        self.current_user = get_current_user()

    def get(self, vehicle_id):
        if vehicle_id:
            vehicle = Vehicle.query.join(Company, aliased=True).filter(Vehicle.id == vehicle_id).filter(
                Company.owner_id == self.current_user.id).first_or_404()
            return vehicle_retrieve_form_schema.dump(vehicle)

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
                owner_id=self.current_user.id).all()
            result = jsonify({'vehicles': vehicle_list_form_schema.dump(vehicles)})
        elif args_driver:
            driver = User.query.filter_by(id=args_driver, chief_id=self.current_user.id).first_or_404()
            result = jsonify({'vehicles': vehicle_list_form_schema.dump(driver.vehicle)})
        elif args_office:
            office = Office.query.filter_by(
                id=args_office).join(Office.company, aliased=True).filter_by(
                owner_id=self.current_user.id).first_or_404()
            result = jsonify({'vehicles': vehicle_list_form_schema.dump(office.vehicles)})
        else:
            company = Company.query.filter_by(owner_id=self.current_user.id).first_or_404()
            result = jsonify({'vehicles': vehicle_list_form_schema.dump(company.vehicles)})
        return result

    def post(self, **kwargs):
        data = validate_request_data(vehicle_create_form_schema)
        license_plate = data.get('license_plate')
        office_id = data.get('office_id')
        company = Company.query.filter_by(owner_id=self.current_user.id).first()
        if Vehicle.check_on_unique_license_plate(license_plate):
            return {'message': f'Vehicle with license plate {license_plate} already exists'}
        if office_id and not company.check_office_exists(office_id):
            abort(Response(f'Office with id = {office_id} not exists in company', 400))
        driver = User.query.filter_by(id=data.get('driver_id'), office_id=office_id).first()
        new_vehicle = Vehicle(
            license_plate=license_plate,
            name=data.get('name'),
            model=data.get('model'),
            year_of_manufacture=data.get('year_of_manufacture'),
            company_id=company.id,
            office_id=office_id
        )
        if driver and office_id:
            new_vehicle.driver.append(driver)
        new_vehicle.save_to_db()
        return {'message': f'Vehicle {new_vehicle.license_plate} {new_vehicle.name} was created'}

    def put(self, vehicle_id):
        data = validate_request_data(vehicle_update_form_schema)
        office_id = data.get('office_id')
        driver_id = data.get('driver_id')
        driver = None
        company = Company.query.filter_by(owner_id=self.current_user.id).first()
        if office_id and not company.check_office_exists(office_id):
            abort(Response(f'Office with id = {office_id} not exists in company', 400))
        if driver_id:
            driver = User.query.filter_by(id=driver_id, office_id=office_id).first()
            if not driver:
                abort(Response(f'You can not assign driver to this vehicle', 400))
        vehicle = Vehicle.query.join(Company, aliased=True).filter(Vehicle.id == vehicle_id).filter(
            Company.owner_id == self.current_user.id).first_or_404()
        for key, value in data.items():
            setattr(vehicle, key, value)
        if driver:
            vehicle.driver.append(driver)
        vehicle.save_to_db()
        return {'message': f'Vehicle {vehicle.name} {vehicle.license_plate} has been updated'}

    def delete(self, vehicle_id):
        vehicle = Vehicle.query.join(Company, aliased=True).filter(Vehicle.id == vehicle_id).filter(
            Company.owner_id == self.current_user.id).first_or_404()
        vehicle.delete_from_db()
        return {'message': f'Vehicle {vehicle.name} {vehicle.license_plate} has been deleted'}, 200


vehicle_view = AdminVehicleView.as_view('vehicle_view_api')
worker_vehicles_view = MyVehiclesView.as_view('my_vehicle_view_api')
