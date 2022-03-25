import json
from app import Company, User
from tests.conftest import admin_user, admin_data, company_1_data, worker_1_user


def test_create_admin(test_client):
    response = test_client.post('/api/admin/registration/', json=admin_data)
    assert response.status_code == 201
    assert response.json['message'] == f"User {admin_data['email']} was created"
    created_admin = User.query.filter_by(email=admin_data.get('email')).first()
    assert created_admin.email == admin_data.get('email')
    assert created_admin.first_name == admin_data.get('first_name')
    assert created_admin.last_name == admin_data.get('last_name')
    #assert created_admin.password == sha256.hash(data.get('password'))
    assert created_admin.is_staff() is False


def test_can_not_create_admin_twice(test_client, init_test_database):
    test_client.post('/api/admin/registration/', json=admin_data)
    response = test_client.post('/api/admin/registration/', json=admin_data)
    assert response.status_code == 400

    assert response.json['message'] == "User with elon@admin.com email already exists"


def test_can_not_create_admin_if_passwords_doesnt_match(test_client, init_test_database):
    admin_data['confirm_password'] = 'incorrect password'
    response = test_client.post('/api/admin/registration/', json=admin_data)
    assert response.status_code == 400
    assert response.data == b'Passwords did not matched'


def test_admin_can_create_company(test_client, admin_token):
    response = test_client.post('/api/company/', headers=admin_token, json=company_1_data)
    assert response.status_code == 201
    assert response.json['message'] == "Company TestCompany was created"
    company = Company.query.filter_by(name=company_1_data['name']).first()
    assert company.name == company_1_data.get('name')
    assert company.address == company_1_data.get('address')
    assert company.owner_id == admin_user.id
    # Because worker defined in setup
    worker_1_user.company_id = admin_user.company_id
    worker_1_user.save_to_db()
    # Because worker defined in setup
    worker_1_user.chief_id = admin_user.id
    worker_1_user.save_to_db()


def test_admin_can_not_create_same_company(test_client, init_test_database, admin_token):
    response = test_client.post('/api/company/', headers=admin_token, json=company_1_data)
    assert response.status_code == 400
    assert response.json['message'] == "Company with name TestCompany already exists"


def test_admin_can_not_create_second_company(test_client, init_test_database, admin_token):
    data = {"name": "SecondTestCompany", "address": "address123445"}
    response = test_client.post('/api/company/', headers=admin_token, json=data)
    assert response.status_code == 400
    assert response.json['message'] == "User admin@test.com has already created a company"


def test_worker_can_not_create_company(test_client, init_test_database, worker_token):
    data = {"name": "WorkerCompany", "address": "address123445"}
    response = test_client.post('/api/company/', headers=worker_token, json=data)
    assert response.status_code == 403
    assert response.data == b'Administrator permission required'


def test_admin_can_view_own_company(test_client, init_test_database, admin_token):
    response = test_client.get('/api/company/', headers=admin_token)
    json_response = json.loads(response.data)
    assert response.status_code == 200
    assert company_1_data['name'] == json_response['name']
    assert company_1_data['address'] == json_response['address']
    assert admin_user.company_id == json_response['id']


def test_worker_can_view_his_company(test_client, init_test_database, worker_json_access_token):
    response = test_client.get('/api/company/', headers=worker_json_access_token)
    json_response = json.loads(response.data)
    assert response.status_code == 200
    assert company_1_data['name'] == json_response['name']
    assert company_1_data['address'] == json_response['address']
    assert admin_user.company_id == json_response['id']


def test_worker_can_not_update_own_company(test_client, init_test_database, worker_json_access_token):
    updated_company_1_data = {"name": "TryingUpdateTestCompany", "address": "TryUpdatedAddress123445"}
    response = test_client.put('/api/company/', headers=worker_json_access_token, json=updated_company_1_data)
    assert response.status_code == 403
    assert response.data == b'Administrator permission required'
    company = Company.query.filter_by(name=company_1_data['name']).first()
    assert company.name == company_1_data.get('name')
    assert company.address == company_1_data.get('address')
    assert company.owner_id == admin_user.id


def test_admin_can_update_own_company(test_client, init_test_database, admin_token):
    updated_company_1_data = {"name": "UpdatedTestCompany", "address": "UpdatedAddress123445"}
    response = test_client.put('/api/company/', headers=admin_token, json=updated_company_1_data)
    assert response.status_code == 200
    assert response.json['message'] == f"Company {updated_company_1_data['name']} has been updated"
    company = Company.query.filter_by(name=updated_company_1_data['name']).first()
    assert company.name == updated_company_1_data.get('name')
    assert company.address == updated_company_1_data.get('address')
    assert company.owner_id == admin_user.id

