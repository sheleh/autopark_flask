
def test_admin_can_login(test_client):
    data = {"email": "admin@test.com", "password": "password"}
    response = test_client.post('/api/login', json=data)
    access_token = response.get_json()["access_token"]
    access_headers = {"Authorization": "Bearer {}".format(access_token)}
    print(test_client)
    assert response.status_code == 200
    assert response.json['message'] == "Logged in as admin@test.com"
    assert len(access_headers) > 0


def test_admin_can_not_login_with_wrong_password(test_client):
    data = {"email": "admin@test.com", "password": "wrong password"}
    response = test_client.post('/api/login', json=data)
    assert response.status_code == 403
    assert response.json['message'] == "Wrong Credentials"


def test_worker_can_login(test_client):
    data = {"email": "worker1@test.com", "password": "password"}
    response = test_client.post('/api/login', json=data)
    access_token = response.get_json()["access_token"]
    access_headers = {"Authorization": "Bearer {}".format(access_token)}
    assert response.status_code == 200
    assert response.json['message'] == f"Logged in as {data['email']}"
    assert len(access_headers) > 0


# def test_admin_can_logout(test_client, init_test_database, admin_token):
#     data = {"email": "admin@test.com", "password": "wrong password"}
#     response = test_client.post('/logout', json=data, headers=admin_token)
#     assert response.status_code == 200
#     assert response.json['message'] == "Access token has been revoked"
#     test_response = test_client.post('/company/', headers=admin_token, json=data)
#     assert test_response.status_code == 401

