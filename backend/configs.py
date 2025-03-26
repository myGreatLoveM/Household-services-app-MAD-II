import os
from pathlib import Path
import datetime
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR/".env")


class Config:
    APP = os.environ.get("FLASK_APP", "main")
    DEBUG = False
    TESTING = False
    RUN_HOST = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    RUN_PORT = os.environ.get("FLASK_RUN_PORT", 8000)
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SECURITY_PASSWORD_HASH = os.environ.get("SECURITY_PASSWORD_HASH")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES")))
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES"))) 
    JWT_BLACKLIST_ENABLED=True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO=False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = BASE_DIR/"static"
    TEMPLATES_FOLDER = BASE_DIR/"templates"
    MIGRATE_FOLDER = BASE_DIR/"migrations"
    USE_SESSION_FOR_NEXT = True
    ITEMS_PER_PAGE = 6
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*') 


class CeleryConfig():
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/1'
    broker_connection_retry_on_startup = True
    timezone = 'Asia/Kolkata'


class DevelopmentConfig(Config, CeleryConfig):
    FLASK_ENV = 'development'
    DEBUG = True
  
    
class ProductionConfig(Config, CeleryConfig):
    FLASK_ENV = 'production'
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config, CeleryConfig):
    FLASK_ENV = 'testing'
    TESTING = True



# app.config['JWT_SECRET_KEY'] = 'jwtsecretkey'  # JWT secret key
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)  # Token expiry
# app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=7)  # Refresh token expiry
# app.config['JWT_BLACKLIST_ENABLED'] = True  # Enable blacklist



# app.config['SECURITY_REGISTERABLE'] = True
# app.config['SECURITY_SEND_REGISTER_EMAIL'] = False