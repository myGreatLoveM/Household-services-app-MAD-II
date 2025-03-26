from flask import jsonify, request
from urllib.parse import urlencode
import re
import time


EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def is_valid_email(email):
    return re.match(EMAIL_REGEX, email)


# Helper function to generate cache key based on endpoint and parameters
def make_cache_key():
    args = request.args
    return f"{request.path}?page={args.get('page')}&per_page={args.get('per_page')}"


# Helper function to generate cache key based on all query parameters
def make_cache_key_with_query_params():
    args = request.args
    query_params = {key: args.get(key) for key in sorted(args)}
    return f"{request.path}?{urlencode(query_params)}"             


def success_response(data={}, message='', is_restful=True, sleep=False, sleep_time_in_sec=1, status_code=200):
    resp = {
        "success": True,
        "data": data
    }
    if message:
        resp["message"] = message

    if sleep:
        time.sleep(sleep_time_in_sec)
        
    if is_restful:
        return resp, status_code
    
    return jsonify(resp), status_code


def error_response(err_message='', errors={}, status_code=500):
    resp = {
        "success": False,
        "err_message": err_message,
        "errors": errors 
    }
    
    return resp, status_code