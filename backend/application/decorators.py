from flask_jwt_extended import current_user, get_current_user, get_jwt_identity
from functools import wraps

from application.utils import error_response
from application.enums import UserRoleEnum


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user is None or role != current_user.roles[0].name:
                return error_response('Access denied, you are not authorized!!', status_code=403)
            
            if current_user.roles[0].name == UserRoleEnum.PROVIDER.value:
                provider = current_user.provider
                if provider.id != kwargs.get('prov_id'):
                    return error_response('Access denied, you are not authorized for others resource!!', status_code=403)

            if current_user.roles[0].name == UserRoleEnum.CUSTOMER.value:
                customer = current_user.customer
                if customer.id != kwargs.get('cust_id'):
                    return error_response('Access denied, you are not authorized for others resource!!', status_code=403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator



   