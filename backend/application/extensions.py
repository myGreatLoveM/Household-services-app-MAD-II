from flask import current_app, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_security import Security
from flask_cors import CORS 
from flask_jwt_extended import JWTManager
from flask_caching import Cache


from application.utils import error_response

db = SQLAlchemy()

migrate = Migrate()

jwt = JWTManager()

security = Security()

cors = CORS()

ma = Marshmallow()

cache = Cache()



@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return error_response("The token has expired, please refresh or log in again.", errors={"token_type": jwt_payload['type']}, status_code=401)


@jwt.unauthorized_loader
def unauthorized_callback(error_message):
    return error_response("Authorization required, no token provided.", status_code=401)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id  


@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = current_app.security.datastore.find_user(id=identity)
    return user