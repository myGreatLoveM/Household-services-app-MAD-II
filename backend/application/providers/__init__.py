from flask import Blueprint
from flask_restful import Api

provider = Blueprint('provider', __name__)

api = Api(provider)

from .resources import ServiceAPI

api.add_resource(ServiceAPI, "/services")
