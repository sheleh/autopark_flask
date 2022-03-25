import pytest
from app import create_app, db, User
from passlib.hash import pbkdf2_sha256 as sha256
from config import TestingConfig

admin_data = {
        "email": "elon@admin.com",
        "first_name": "Elon",
        "last_name": "Musk",
        "password": "password",
        "confirm_password": "password"
    }

worker_data = {
        "email": "firstworker@worker.com",
        "first_name": "Django",
        "last_name": "Freeman",
        "password": "password",
    }

worker_2_data = {
        "email": "secondworker@worker.com",
        "first_name": "Calvin",
        "last_name": "Candy",
        "password": "password",
    }

office_1_data = {
    'name': "Tesla Factory",
    'address': "46 Avenue",
    'country': "USA",
    'city': "Texas",
    'region': "TA",
}

office_2_data = {
    "name": "Tesla Australia & New Zealand",
    "address": "Blue Street 14",
    "country": "Australia",
    "city": "Sydney",
    "region": "NSW"
}

vehicle_1_data = {
    "license_plate": "T999",
    "name": "Tesla",
    "model": "Model X",
    "year_of_manufacture": 2020
}

vehicle_2_data = {
    "license_plate": "T1000",
    "name": "Tesla",
    "model": "Model S",
    "year_of_manufacture": 2019
}

updated_vehicle_2_data = {
    "license_plate": "EK10098",
    "name": "Tesla",
    "model": "S",
    "year_of_manufacture": 2019,
}


company_1_data = {"name": "TestCompany", "address": "address123445"}

admin_user = User(
        email='admin@test.com',
        first_name="flaskyflask",
        last_name='flaskow',
        password=sha256.hash('password'),
        chief_id=None,
        company_id=None,
        office_id=None,
    )

worker_1_user = User(
        email='worker1@test.com',
        first_name="Dalai",
        last_name='Llama',
        password=sha256.hash('password'),
        chief_id=None,
        company_id=None,
        office_id=None,
    )


def clear_db_data(session):
    meta = db.metadata
    for table in meta.sorted_tables:
        session.execute(table.delete())
    session.commit()


@pytest.fixture(scope='session')
def init_test_database():

    clear_db_data(db.session)
    db.session.begin()
    db.create_all()
    db.session.add(admin_user)
    db.session.add(worker_1_user)
    yield db.session
    db.session.rollback()
    clear_db_data(db.session)

    # clear_db_data(db.session)
    # savepoint1 = db.session.begin_nested()
    # engine = db.engine
    # db.app = test_client
    # meta = db.metadata
    # test_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    # #db.drop_all()
    # clear_db_data(test_session)
    # #db.session.begin()
    # #db.create_all()
    # test_session.add(admin_user)
    # test_session.add(worker_1_user)
    # test_session.commit()
    # #db.session.flush()
    # yield test_session
    #
    # test_session.close()
    # test_session.remove()
    # savepoint1.rollback()
    # # db.session.remove()
    # # db.session.close()
    # #db.session.remove()
    # clear_db_data(db.session)


@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app()
    flask_app.config.from_object(TestingConfig)

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope='session')
def admin_json_access_token(test_client, init_test_database):
    data = {"email": "admin@test.com", "password": "password"}
    response = test_client.post('/api/login', json=data)
    access_token = response.json['access_token']
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }


@pytest.fixture(scope='session')
def worker_json_access_token(test_client, init_test_database):
    data = {"email": "worker1@test.com", "password": "password"}
    response = test_client.post('/api/login', json=data)
    access_token = response.json['access_token']
    return {
        'Authorization': f'Bearer {access_token}'
    }


admin_token = admin_json_access_token
worker_token = worker_json_access_token
