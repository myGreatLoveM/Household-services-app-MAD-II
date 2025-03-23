from flask import Blueprint, jsonify
from.utils import error_response

error_bp = Blueprint('error_handlers', __name__)


# 404 Not Found Handler
@error_bp.app_errorhandler(404)
def not_found_error(error):
    return error_response("The requested resource was not found.", {"error": "Not Found"}, status_code=404)


# 500 Internal Server Error Handler
@error_bp.app_errorhandler(500)
def internal_server_error(error):
    return error_response("An internal server error occurred.", {"error": "Internal Server Error"}, status_code=500)


# 403 Forbidden Error Handler
@error_bp.app_errorhandler(403)
def forbidden_error(error):
    return error_response("You don't have permission to access this resource.", {"error": "Forbidden"}, status_code=403)


# 401 Unauthorized Error Handler
@error_bp.app_errorhandler(401)
def unauthorized_error(error):
    return error_response("You need to log in to access this resource.", {"error": "Unauthorized"}, status_code=403)