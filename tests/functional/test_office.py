import json
from app import Office
from tests.conftest import admin_user, worker_1_user, office_2_data, office_1_data


def test_admin_can_create_office(test_client, init_test_database, admin_token):
    response = test_client.post('/api/offices/', headers=admin_token, json=office_1_data)
    assert response.status_code == 201
    assert response.json['message'] == f"Office with name {office_1_data['name']} was created"
    office = Office.query.filter_by(name=office_1_data['name']).first()
    assert office.name == office_1_data.get('name')
    assert office.address == office_1_data.get('address')
    assert office.country == office_1_data.get('country')
    assert office.city == office_1_data.get('city')
    assert office.region == office_1_data.get('region')
    assert office.company_id == admin_user.company_id


def test_admin_can_create_second_office(test_client, init_test_database, admin_token):
    response = test_client.post('/api/offices/', headers=admin_token, json=office_2_data)
    assert response.status_code == 201
    assert response.json['message'] == f"Office with name {office_2_data['name']} was created"
    office = Office.query.filter_by(name=office_2_data['name']).first()
    assert office.name == office_2_data.get('name')
    assert office.address == office_2_data.get('address')
    assert office.country == office_2_data.get('country')
    assert office.city == office_2_data.get('city')
    assert office.region == office_2_data.get('region')
    assert office.company_id == admin_user.company_id


def test_admin_can_view_list_of_offices(test_client, init_test_database, admin_token):
    response = test_client.get('/api/offices/', headers=admin_token)
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert office_1_data['name'] == json_response['offices'][0]['name']
    assert office_1_data['address'] == json_response['offices'][0]['address']
    assert office_1_data['country'] == json_response['offices'][0]['country']
    assert office_1_data['city'] == json_response['offices'][0]['city']
    assert office_1_data['region'] == json_response['offices'][0]['region']
    assert office_2_data['name'] == json_response['offices'][1]['name']
    assert office_2_data['address'] == json_response['offices'][1]['address']
    assert office_2_data['country'] == json_response['offices'][1]['country']
    assert office_2_data['city'] == json_response['offices'][1]['city']
    assert office_2_data['region'] == json_response['offices'][1]['region']


def test_admin_can_filter_offices_by_country(test_client, init_test_database, admin_token):
    country_key = office_1_data['country']
    response = test_client.get(f'/api/offices/?country={country_key}', headers=admin_token)
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert office_1_data['name'] == json_response['offices'][0]['name']
    assert office_1_data['address'] == json_response['offices'][0]['address']
    assert office_1_data['country'] == json_response['offices'][0]['country']
    assert office_1_data['city'] == json_response['offices'][0]['city']
    assert office_1_data['region'] == json_response['offices'][0]['region']
    assert len(json_response['offices']) == 1


def test_admin_can_filter_offices_by_city(test_client, init_test_database, admin_token):
    city_key = office_2_data['city']
    response = test_client.get(f'/api/offices/?city={city_key}', headers=admin_token)
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert office_2_data['name'] == json_response['offices'][0]['name']
    assert office_2_data['address'] == json_response['offices'][0]['address']
    assert office_2_data['country'] == json_response['offices'][0]['country']
    assert office_2_data['city'] == json_response['offices'][0]['city']
    assert office_2_data['region'] == json_response['offices'][0]['region']
    assert len(json_response['offices']) == 1


def test_admin_can_filter_offices_by_city_and_country(test_client, init_test_database, admin_token):
    city_key = office_2_data['city']
    country_key = office_2_data['country']
    response = test_client.get(f'/api/offices/?city={city_key}&country={country_key}', headers=admin_token)
    json_response = json.loads(response.data)
    assert response.status_code == 200
    assert office_2_data['name'] == json_response['offices'][0]['name']
    assert office_2_data['address'] == json_response['offices'][0]['address']
    assert office_2_data['country'] == json_response['offices'][0]['country']
    assert office_2_data['city'] == json_response['offices'][0]['city']
    assert office_2_data['region'] == json_response['offices'][0]['region']
    assert len(json_response['offices']) == 1


def test_admin_can_retrieve_office_information(test_client, admin_token):
    test_office = Office.query.filter_by(name=office_1_data['name']).first()
    response = test_client.get(f'/api/offices/{test_office.id}', headers=admin_token)
    json_response = json.loads(response.data)
    assert response.status_code == 200
    assert test_office.name == json_response['name']
    assert test_office.address == json_response['address']
    assert test_office.country == json_response['country']
    assert test_office.city == json_response['city']
    assert test_office.region == json_response['region']
    assert test_office.company_id == admin_user.company_id


def test_worker_can_not_retrieve_office_information(test_client, worker_token):
    test_office = Office.query.filter_by(name=office_1_data['name']).first()
    response = test_client.get(f'/api/offices/{test_office.id}', headers=worker_token)
    assert response.status_code == 403
    assert response.json['message'] == "Administrator permissions required"


def test_worker_can_not_update_office_information(test_client, worker_token):
    test_office = Office.query.filter_by(name=office_1_data['name']).first()
    updated_office_1_data = {
        "name": "Mega Factory",
        "address": "Mega address",
        "country": "England",
        "city": "London",
        "region": "MN",
    }
    response = test_client.put(f'/api/offices/{test_office.id}', headers=worker_token, json=updated_office_1_data)
    assert response.status_code == 403
    assert response.data == b'Administrator permission required'


def test_admin_can_update_office_information(test_client, admin_token):
    test_office = Office.query.filter_by(name=office_1_data['name']).first()
    updated_office_1_data = {
        "name": "Mega Factory",
        "address": "Mega address",
        "country": "England",
        "city": "London",
        "region": "MN",
    }
    response = test_client.put(f'/api/offices/{test_office.id}', headers=admin_token, json=updated_office_1_data)
    assert response.status_code == 200
    assert response.json['message'] == f"Office {test_office.name} has been updated"
    assert test_office.name == updated_office_1_data['name']
    assert test_office.address == updated_office_1_data['address']
    assert test_office.country == updated_office_1_data['country']
    assert test_office.city == updated_office_1_data['city']
    assert test_office.region == updated_office_1_data['region']
    assert test_office.name != office_1_data['name']
    assert test_office.address != office_1_data['address']
    assert test_office.country != office_1_data['country']
    assert test_office.city != office_1_data['city']
    assert test_office.region != office_1_data['region']


def test_admin_can_assign_worker_to_office(test_client, admin_token):
    test_office = Office.query.filter_by(name=office_2_data['name']).first()
    response = test_client.put(f'/api/offices/{test_office.id}/assign/{worker_1_user.id}', headers=admin_token)
    assert response.status_code == 200
    assert response.json['message'] == f"User {worker_1_user.email} has been assigned to {test_office.name}"
    assert worker_1_user.office_id == test_office.id
    assert worker_1_user.company_id == test_office.company_id


def test_worker_can_view_his_office_information(test_client, worker_token):
    test_office = Office.query.filter_by(id=worker_1_user.office_id).first()
    response = test_client.get('/api/my_office/', headers=worker_token)
    json_response = json.loads(response.data)
    assert response.status_code == 200
    assert test_office.name == json_response['name']
    assert test_office.address == json_response['address']
    assert test_office.country == json_response['country']
    assert test_office.city == json_response['city']
    assert test_office.region == json_response['region']
    assert test_office.company_id == admin_user.company_id
