import os
from datetime import timedelta


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    host = os.environ.get('POSTGRES_HOST')
    database = os.environ.get('POSTGRES_DB')
    port = os.environ.get('POSTGRES_PORT')
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    DATABASE_URL = f"postgresql+psycopg2://{host}/{database}"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = os.environ.get('DEBUG')
    FLASK_ENV = os.environ.get('FLASK_ENV')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'Testsecretkey'

