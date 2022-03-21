import json
from app import User
from tests.conftest import admin_user, worker_data, worker_2_data, worker_1_user


def test_admin_can_create_worker(test_client, init_test_database, admin_token):
    response = test_client.post('/api/users/', headers=admin_token, json=worker_data)
    assert response.status_code == 201
    assert response.json['message'] == f"User {worker_data['email']} was created"
    worker = User.query.filter_by(email=worker_data['email']).first()
    assert worker.email == worker_data.get('email')
    assert worker.first_name == worker_data.get('first_name')
    assert worker.last_name == worker_data.get('last_name')
    assert worker.chief_id == admin_user.id
    assert worker.company_id == admin_user.company.id
    assert worker.is_stafff is True


def test_admin_can_not_create_second_worker_with_same_email(test_client, init_test_database, admin_token):
    response = test_client.post('/api/users/', headers=admin_token, json=worker_data)
    assert response.status_code == 400
    assert response.data == b'User with firstworker@worker.com email already exists'
    assert User.query.filter_by(email=worker_data['email']).first()


def test_admin_can_create_second_worker(test_client, init_test_database, admin_token):
    response = test_client.post('/api/users/', headers=admin_token, json=worker_2_data)
    assert response.status_code == 201
    assert response.json['message'] == f"User {worker_2_data['email']} was created"
    worker = User.query.filter_by(email=worker_2_data['email']).first()
    assert worker.email == worker_2_data.get('email')
    assert worker.first_name == worker_2_data.get('first_name')
    assert worker.last_name == worker_2_data.get('last_name')
    assert worker.chief_id == admin_user.id
    assert worker.company_id == admin_user.company.id
    assert worker.is_stafff is True


def test_admin_can_view_list_of_workers(test_client, admin_token):
    response = test_client.get('/api/users/', headers=admin_token)
    json_response = json.loads(response.data)
    assert worker_1_user.email == json_response['users'][0]['email']
    assert worker_1_user.first_name == json_response['users'][0]['first_name']
    assert worker_1_user.last_name == json_response['users'][0]['last_name']
    assert worker_1_user.company_id == json_response['users'][0]['company_id']
    assert worker_data['email'] == json_response['users'][1]['email']
    assert worker_data['first_name'] == json_response['users'][1]['first_name']
    assert worker_data['last_name'] == json_response['users'][1]['last_name']
    assert admin_user.company_id == json_response['users'][1]['company_id']
    assert worker_2_data['email'] == json_response['users'][2]['email']
    assert worker_2_data['first_name'] == json_response['users'][2]['first_name']
    assert worker_2_data['last_name'] == json_response['users'][2]['last_name']
    assert admin_user.company_id == json_response['users'][2]['company_id']
    assert response.status_code == 200


def test_admin_can_filter_workers_by_first_name(test_client, admin_token):
    key = worker_data['first_name']
    response = test_client.get(f'/api/users/?first_name={key}', headers=admin_token)
    json_response = json.loads(response.data)
    assert worker_data['email'] == json_response['users'][0]['email']
    assert worker_data['first_name'] == json_response['users'][0]['first_name']
    assert worker_data['last_name'] == json_response['users'][0]['last_name']
    assert admin_user.company_id == json_response['users'][0]['company_id']
    assert response.status_code == 200


def test_admin_can_filter_workers_by_last_name(test_client, admin_token):
    key = worker_data['last_name']
    response = test_client.get(f'/api/users/?last_name={key}', headers=admin_token)
    json_response = json.loads(response.data)
    assert worker_data['email'] == json_response['users'][0]['email']
    assert worker_data['first_name'] == json_response['users'][0]['first_name']
    assert worker_data['last_name'] == json_response['users'][0]['last_name']
    assert admin_user.company_id == json_response['users'][0]['company_id']
    assert response.status_code == 200


def test_admin_can_filter_workers_by_email(test_client, admin_token):
    key = worker_data['email']
    response = test_client.get(f'/api/users/?email={key}', headers=admin_token)
    json_response = json.loads(response.data)
    assert worker_data['email'] == json_response['users'][0]['email']
    assert worker_data['first_name'] == json_response['users'][0]['first_name']
    assert worker_data['last_name'] == json_response['users'][0]['last_name']
    assert admin_user.company_id == json_response['users'][0]['company_id']
    assert response.status_code == 200


def test_worker_can_not_view_list_of_workers(test_client, worker_token):
    response = test_client.get('/api/users/', headers=worker_token)
    assert response.data == b'Administrator permission required'


def test_admin_can_view_worker_information(test_client, admin_token):
    worker_user_id = User.query.filter_by(email='firstworker@worker.com').first()
    response = test_client.get(f'/api/users/{worker_user_id.id}', headers=admin_token)
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert worker_data['email'] == json_response['email']
    assert worker_data['first_name'] == json_response['first_name']
    assert worker_data['last_name'] == json_response['last_name']
    assert admin_user.company_id == json_response['company_id']


def test_admin_can_update_worker_information(test_client, admin_token):
    worker = User.query.filter_by(email='firstworker@worker.com').first()
    old_password = worker.password
    updated_worker_data = {
        "first_name": "John",
        "last_name": "Varvatos",
        "password": "updatedpassword",
    }
    response = test_client.put(f'/api/users/{worker.id}', headers=admin_token, json=updated_worker_data)
    assert response.status_code == 200
    assert response.json['message'] == "User has been updated"
    assert worker.first_name == updated_worker_data['first_name']
    assert worker.last_name == updated_worker_data['last_name']
    assert worker.password != old_password


def test_admin_can_not_update_worker_email(test_client, admin_token):
    worker = User.query.filter_by(email='firstworker@worker.com').first()
    updated_worker_data = {
        "email": "iwannachangeemail@wmail.com",
    }
    response = test_client.put(f'/api/users/{worker.id}', headers=admin_token, json=updated_worker_data)
    assert response.status_code == 400


def test_worker_can_not_delete_worker(test_client, worker_token):
    worker = User.query.filter_by(email='secondworker@worker.com').first()
    response = test_client.delete(f'/api/users/{worker.id}', headers=worker_token)
    assert response.data == b'Administrator permission required'
    assert response.status_code == 403


def test_admin_can_delete_worker(test_client, admin_token):
    worker = User.query.filter_by(email='secondworker@worker.com').first()
    response = test_client.delete(f'/api/users/{worker.id}', headers=admin_token)
    assert response.status_code == 200
    assert response.json['message'] == "User has been deleted"
    assert User.query.filter_by(email='secondworker@worker.com').first() is None


def test_admin_can_view_own_profile(test_client, admin_token):
    response = test_client.get(f'/api/profile/', headers=admin_token)
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert admin_user.email == json_response['email']
    assert admin_user.first_name == json_response['first_name']
    assert admin_user.last_name == json_response['last_name']


def test_worker_can_view_own_profile(test_client, worker_token):
    response = test_client.get(f'/api/profile/', headers=worker_token)
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert worker_1_user.email == json_response['email']
    assert worker_1_user.first_name == json_response['first_name']
    assert worker_1_user.last_name == json_response['last_name']


def test_admin_can_update_own_profile(test_client, admin_token):
    old_password = admin_user.password
    updated_profile_data = {
        "first_name": "UpdatedProfileName",
        "last_name": "UpdatedProfileFirstName",
        "password": "updatedpassword",
    }
    response = test_client.put(f'/api/profile/', headers=admin_token, json=updated_profile_data)
    assert response.status_code == 200
    assert response.json['message'] == f"User {admin_user.email} has been updated"
    assert admin_user.first_name == updated_profile_data['first_name']
    assert admin_user.last_name == updated_profile_data['last_name']
    assert admin_user.password != old_password


def test_worker_can_update_own_profile(test_client, worker_token):
    old_password = worker_1_user.password
    updated_profile_data = {
        "first_name": "UpdatedWorkerProfileName",
        "last_name": "UpdatedWorkerProfileFirstName",
        "password": "updatedpassword",
    }
    response = test_client.put(f'/api/profile/', headers=worker_token, json=updated_profile_data)
    assert response.status_code == 200
    assert response.json['message'] == f"User {worker_1_user.email} has been updated"
    assert worker_1_user.first_name == updated_profile_data['first_name']
    assert worker_1_user.last_name == updated_profile_data['last_name']
    assert worker_1_user.password != old_password

