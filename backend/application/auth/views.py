from flask import request, current_app, jsonify, make_response
from flask_security import SQLAlchemyUserDatastore, verify_password, hash_password
from flask_jwt_extended import create_access_token, create_refresh_token, current_user, jwt_required, get_jwt_identity, verify_jwt_in_request
from marshmallow import ValidationError
import time


from . import auth
from application.core.models import Profile, User
from application.admin.models import Category
from application.customers.models import Customer
from application.providers.models import Provider
from application.utils import success_response, error_response
from application.extensions import db
from application.auth.schemas import UserRegisterSchema, ProviderRegisterSchema, UserLoginSchema
from application.enums import UserGenderEnum, UserRoleEnum
from application.core.schemas import UserSchema


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    schema = UserLoginSchema()
    
    try:
        val_data = schema.load(data)

        username = val_data.get('username')
        password = val_data.get('password')

        datastore = current_app.security.datastore
        user = datastore.find_user(username=username)

        if not user:
            return error_response('user not exists, invalid credentials', status_code=401)
        
        is_password_true = verify_password(password, user.password_hash)

        if is_password_true:
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)

            user_data = UserSchema().dump(user)

            data = {
                "user": user_data,
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            print(data)
            time.sleep(3)
            return success_response(data, 'user logged in successfully', status_code=201)
        else:
            return error_response('wrong password, invalid credentials', status_code=401)
    except ValidationError as err:
        return error_response('validation errors', errors=err.messages, status_code=400)
    except Exception as e:
        print(e)
        return error_response('something went wrong, please try again', status_code=500)


@auth.route('/register/<role>', methods=['POST'])
def register(role):
    data = request.get_json()

    if not role:
        return error_response('role is required to register user', status_code=400)
    elif role not in [role.value for role in UserRoleEnum]:
        return error_response('no such role exists, please try again', status_code=400)

    schema = None
    if role == UserRoleEnum.PROVIDER.value:
        schema = ProviderRegisterSchema()
    else:
        schema = UserRegisterSchema()

    try:
        val_data = schema.load(data)
        
        username = val_data.get('username')
        email = val_data.get('email')
        password = val_data.get('password')
        gender = val_data.get('gender')
        location = val_data.get('location')
        contact = val_data.get('contact')

        datastore = current_app.security.datastore

        user = db.session.query(User).filter(db.or_(User.username == username, User.email == email)).first()

        if user:
            return error_response('user already exists, please try login', status_code=409)
        
        new_user = datastore.create_user(
            username=username, email=email, password_hash=hash_password(password), roles=[role], active=True
        )

        profile = Profile(sex=gender, location=location, contact=contact)
        new_user.profile = profile

        if role == UserRoleEnum.CUSTOMER.value:
            new_customer = Customer()
            new_user.customer = new_customer
        
        elif role == UserRoleEnum.PROVIDER.value:
            category = val_data.get('category')
            experience = val_data.get('experience')

            category_obj = Category.query.filter_by(name=category).first()
            new_provider = Provider(experience=int(experience))

            new_user.provider = new_provider
            category_obj.providers.append(new_provider)
        db.session.commit()
        time.sleep(3)
        return success_response(message='user registered successfully', status_code=201)
    except ValidationError as err:
        return error_response('validation errors', errors=err.messages, status_code=400)
    except:
        db.session.rollback()
        return error_response('something went wrong, while registering user', status_code=500)
    
    

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@auth.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    access_token = create_access_token(identity=current_user)
    refresh_token = create_refresh_token(identity=current_user)
    data = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return success_response(data, f'both tokens refreshed for user id {current_user.id}', status_code=201)
    








# # @auth.route('/protected', methods=['GET'])
# # @jwt_required()  # Requires access token
# # def protected():
# #     # Get the user ID and fs_uniquifier from the JWT token
# #     current_user_id = get_jwt_identity()
# #     token_fs_uniquifier = get_jwt()["fs_uniquifier"]

# #     # Retrieve the current fs_uniquifier from the database
# #     user = user_datastore.get_user(current_user_id)

# #     # Compare fs_uniquifier from token and database
# #     if user.fs_uniquifier != token_fs_uniquifier:
# #         return jsonify({"msg": "Invalid token, user session has been invalidated."}), 401

# #     return jsonify(logged_in_as=user.email), 200


# # Simplified token blacklist
# # blacklist = set()

# # # Revoke a refresh token (example endpoint)
# # @app.route('/logout', methods=['POST'])
# # @jwt_required(refresh=True)
# # def logout():
# #     jti = get_jwt()["jti"]  # Get the JWT ID (unique identifier) of the token
# #     blacklist.add(jti)       # Add the token to the blacklist
# #     return jsonify({"msg": "Logged out successfully"}), 200

# # # Check if a token is blacklisted
# # @jwt.token_in_blocklist_loader
# # def check_if_token_in_blacklist(jwt_header, jwt_payload):
# #     jti = jwt_payload["jti"]
# #     return jti in blacklist

# # @jwt.revoked_token_loader
# # def revoked_token_callback(jwt_header, jwt_payload):
# #     return jsonify({
# #         "msg": "The token has been revoked. Please log in again."
# #     }), 401


# # @jwt.invalid_token_loader
# # def invalid_token_callback(error_message):
#     return jsonify({
#         "msg": "The provided token is invalid or malformed.",
#         "error": error_message
#     }), 401

# Custom handler for expired tokens (both access and refresh)
