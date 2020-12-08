import os
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY') or '!Turorudi1!'
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME') or '!Blancer2020!'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SENDGRID_API_KEY = environ.get('SENDGRID_API_KEY') or 'APIKEY'


class ProdConfig(Config):
    """Production config."""
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('POSTGRES_URI')


class DevConfig(Config):
    """Development config."""
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = environ.get('DEV_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLITE_URI') or \
                              'sqlite:///' + path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False