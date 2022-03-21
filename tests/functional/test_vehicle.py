import json
from app import Vehicle, Office
from tests.conftest import (
    admin_user,
    worker_1_user,
    vehicle_1_data,
    vehicle_2_data,
    office_2_data,
    updated_vehicle_2_data
)


def test_admin_can_create_vehicle(test_client, init_test_database, admin_token):
    response = test_client.post('/api/vehicles/', headers=admin_token, json=vehicle_1_data)
    vehicle = Vehicle.query.filter_by(license_plate=vehicle_1_data['license_plate']).first()
    assert response.status_code == 200
    assert response.json['message'] == f"Vehicle {vehicle_1_data['license_plate']} {vehicle_1_data['name']} was created"
    assert vehicle.license_plate == vehicle_1_data.get('license_plate')
    assert vehicle.name == vehicle_1_data.get('name')
    assert vehicle.model == vehicle_1_data.get('model')
    assert vehicle.year_of_manufacture == vehicle_1_data.get('year_of_manufacture')
    assert vehicle.company_id == admin_user.company_id
    assert vehicle.office_id is None


def test_admin_can_create_vehicle_with_assigned_driver(test_client, init_test_database, admin_token):
    vehicle_2_data['office_id'] = worker_1_user.office_id
    vehicle_2_data['driver_id'] = worker_1_user.id
    response = test_client.post('/api/vehicles/', headers=admin_token, json=vehicle_2_data)
    vehicle = Vehicle.query.filter_by(license_plate=vehicle_2_data['license_plate']).first()
    assert response.status_code == 200
    assert response.json['message'] == f"Vehicle {vehicle_2_data['license_plate']} {vehicle_2_data['name']} was created"
    assert vehicle.license_plate == vehicle_2_data.get('license_plate')
    assert vehicle.name == vehicle_2_data.get('name')
    assert vehicle.model == vehicle_2_data.get('model')
    assert vehicle.year_of_manufacture == vehicle_2_data.get('year_of_manufacture')
    assert vehicle.company_id == admin_user.company_id
    assert vehicle.driver == [worker_1_user]


def test_admin_can_not_create_vehicle_when_not_assigned_to_offices(test_client, init_test_database, admin_token):
    vehicle_2_data['office_id'] = None
    vehicle_2_data['driver_id'] = worker_1_user.id
    response = test_client.post('/api/vehicles/', headers=admin_token, json=vehicle_2_data)
    assert response.status_code == 400
    assert response.data == b"Incorrect data {'office_id': ['Field may not be null.']}"


def test_worker_can_not_create_vehicle(test_client, init_test_database, worker_token):
    response = test_client.post('/api/vehicles/', headers=worker_token, json=vehicle_2_data)
    assert response.status_code == 403
    assert response.data == b'Administrator permission required'


def test_admin_can_view_list_of_vehicles(test_client, init_test_database, admin_token):
    response = test_client.get('/api/vehicles/', headers=admin_token)
    json_response = json.loads(response.data)
    assert response.status_code == 200
    assert vehicle_1_data['license_plate'] == json_response['vehicles'][0]['license_plate']
    assert vehicle_1_data['model'] == json_response['vehicles'][0]['model']
    assert vehicle_1_data['name'] == json_response['vehicles'][0]['name']
    assert vehicle_1_data['year_of_manufacture'] == json_response['vehicles'][0]['year_of_manufacture']
    assert vehicle_2_data['license_plate'] == json_response['vehicles'][1]['license_plate']
    assert vehicle_2_data['model'] == json_response['vehicles'][1]['model']
    assert vehicle_2_data['name'] == json_response['vehicles'][1]['name']
    assert vehicle_2_data['year_of_manufacture'] == json_response['vehicles'][1]['year_of_manufacture']


def test_admin_can_filter_list_of_vehicles_by_office_and_driver(test_client, init_test_database, admin_token):
    driver_id = worker_1_user.id
    office_id = worker_1_user.office_id
    response = test_client.get(f'/api/vehicles/?driver_id={driver_id}&office_id={office_id}', headers=admin_token)
    json_response = json.loads(response.data)
    assert response.status_code == 200
    assert vehicle_2_data['license_plate'] == json_response['vehicles'][0]['license_plate']
    assert vehicle_2_data['model'] == json_response['vehicles'][0]['model']
    assert vehicle_2_data['name'] == json_response['vehicles'][0]['name']
    assert vehicle_2_data['year_of_manufacture'] == json_response['vehicles'][0]['year_of_manufacture']


def test_admin_can_retrieve_vehicle_information(test_client, admin_token):
    test_vehicle = Vehicle.query.filter_by(license_plate=vehicle_1_data['license_plate']).first()
    response = test_client.get(f'/api/vehicles/{test_vehicle.id}', headers=admin_token)
    json_response = json.loads(response.data)
    assert response.status_code == 200
    assert test_vehicle.license_plate == json_response['license_plate']
    assert test_vehicle.name == json_response['name']
    assert test_vehicle.model == json_response['model']
    assert test_vehicle.year_of_manufacture == json_response['year_of_manufacture']
    assert test_vehicle.company_id == admin_user.company_id


def test_admin_can_update_vehicle_information(test_client, admin_token):
    test_vehicle = Vehicle.query.filter_by(license_plate=vehicle_2_data['license_plate']).first()
    response = test_client.put(f'/api/vehicles/{test_vehicle.id}', headers=admin_token, json=updated_vehicle_2_data)
    assert response.status_code == 200
    assert response.json['message'] == \
           f"Vehicle {updated_vehicle_2_data['name']} {updated_vehicle_2_data['license_plate']} has been updated"
    assert test_vehicle.license_plate == updated_vehicle_2_data['license_plate']
    assert test_vehicle.name == updated_vehicle_2_data['name']
    assert test_vehicle.model == updated_vehicle_2_data['model']
    assert test_vehicle.year_of_manufacture == updated_vehicle_2_data['year_of_manufacture']
    assert test_vehicle.company_id == admin_user.company_id


def test_admin_can_update_vehicle_and_driver_office_information(test_client, admin_token):
    test_vehicle = Vehicle.query.filter_by(license_plate=vehicle_1_data['license_plate']).first()
    office = Office.query.filter_by(name=office_2_data['name']).first()
    updated_vehicle_1_data = {
        "license_plate": vehicle_1_data['license_plate'],
        "name": vehicle_1_data['name'],
        "model": vehicle_1_data['model'],
        "year_of_manufacture": vehicle_1_data['year_of_manufacture'],
        "office_id": office.id,
        "driver_id": worker_1_user.id,
    }
    response = test_client.put(f'/api/vehicles/{test_vehicle.id}', headers=admin_token, json=updated_vehicle_1_data)
    assert response.status_code == 200
    assert response.json['message'] == \
           f"Vehicle {vehicle_1_data['name']} {vehicle_1_data['license_plate']} has been updated"
    assert test_vehicle.license_plate == updated_vehicle_1_data['license_plate']
    assert test_vehicle.name == updated_vehicle_1_data['name']
    assert test_vehicle.model == updated_vehicle_1_data['model']
    assert test_vehicle.year_of_manufacture == updated_vehicle_1_data['year_of_manufacture']
    assert test_vehicle.company_id == admin_user.company_id


def test_worker_can_view_list_of_assigned_vehicles(test_client, init_test_database, worker_token):
    response = test_client.get('/api/my_vehicles/', headers=worker_token)
    json_response = json.loads(response.data)
    assert response.status_code == 200
    assert updated_vehicle_2_data['license_plate'] == json_response['vehicles'][0]['license_plate']
    assert updated_vehicle_2_data['model'] == json_response['vehicles'][0]['model']
    assert updated_vehicle_2_data['name'] == json_response['vehicles'][0]['name']
    assert updated_vehicle_2_data['year_of_manufacture'] == json_response['vehicles'][0]['year_of_manufacture']
    assert vehicle_1_data['license_plate'] == json_response['vehicles'][1]['license_plate']
    assert vehicle_1_data['model'] == json_response['vehicles'][1]['model']
    assert vehicle_1_data['name'] == json_response['vehicles'][1]['name']
    assert vehicle_1_data['year_of_manufacture'] == json_response['vehicles'][1]['year_of_manufacture']

