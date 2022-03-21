import pytest
from app import create_app, db, User
from passlib.hash import pbkdf2_sha256 as sha256
from config import TestingConfig, DevelopmentConfig
from _pytest import monkeypatch
import os
import tempfile


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
        is_stafff=False
    )

worker_1_user = User(
        email='worker1@test.com',
        first_name="Dalai",
        last_name='Llama',
        password=sha256.hash('password'),
        chief_id=None,
        company_id=None,
        office_id=None,
        is_stafff=True
    )


@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app()
    flask_app.config.from_object(TestingConfig)

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


# @pytest.fixture(scope='session')
# def test_client():
#     mp = monkeypatch.MonkeyPatch()
#     mp.setenv("DATABASE_URI", 'postgresql://autopark_su:password@localhost:5432/flask_db')
#     flask_app = create_app()
#     #flask_app.config.from_object(TestingConfig)
#     client = flask_app.test_client()
#     yield client
#     # with flask_app.test_client() as testing_client:
#     #     with flask_app.app_context():
#     #         yield testing_client



# from app import app as flaskr
#
#
# @pytest.fixture
# def db_handle():
#     db_fd, db_fname = tempfile.mkstemp()
#     app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
#     app.app.config["TESTING"] = True
#
#     with app.app.app_context():
#         app.db.create_all()
#
#     yield app.db
#
#     app.db.session.remove()
#     os.close(db_fd)
#     os.unlink(db_fname)
#
#
#
# # import tempfile
# #
# # # Third party imports
# # import pytest
# # from sqlalchemy import create_engine
# # from sqlalchemy.orm import sessionmaker
# # from pytest_postgresql import factories
# #
# #
# # # Using the factory to create a postgresql instance
# # socket_dir = tempfile.TemporaryDirectory()
# # postgresql_my_proc = factories.postgresql_proc(port=None, unixsocketdir=socket_dir.name)
# # postgresql_my = factories.postgresql('postgresql_my_proc')
# #
# #
# # @pytest.fixture(scope='function')
# # def setup_database(postgresql_my):
# #
# #     def dbcreator():
# #         return postgresql_my.cursor().connection
# #
# #     engine = create_engine('postgresql+psycopg2://', creator=dbcreator)
# #     db.create_all(engine)
# #     Session = sessionmaker(bind=engine)
# #     session = Session()
# #     yield session
# #     session.close()
# #
# # @pytest.fixture(scope='function')
# # def dataset(setup_database):
# #
# #     session = setup_database
# #
# #     # Creates user
# #
# #     session.add(admin_user)
# #     session.add(worker_1_user)
# #     session.commit()
# #
# #     # Creates account
# #     session.commit()
# #
# #     yield session
#
#


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
    #db.session.flush()
    yield db.session
    db.session.rollback()
    #db.session.remove()
    clear_db_data(db.session)

# @pytest.fixture(scope="session", autouse=True)
# def fake_db():
#     db_prep()
#     print(f"initializing {DB_NAME}…")
#     engine = create_engine(settings.db_url)
#     from app.models import User
#     from app.database import SessionLocal, Base
#     db = SessionLocal()
#     Base.metadata.create_all(engine)
#     print(f"{DB_NAME} ready to rock!")
#     try:
#         yield db
#     finally:
#         db.close()


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
