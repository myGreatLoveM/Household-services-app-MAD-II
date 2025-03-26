from flask import Blueprint
from flask_restful import Api

provider = Blueprint('provider', __name__)

api = Api(provider)

from .resources import ProviderServiceListAPI, ProviderProfileAPI, ProviderServiceMgmtAPI

api.add_resource(ProviderServiceListAPI, '/services')

api.add_resource(ProviderServiceMgmtAPI, '/services/<int:service_id>')

api.add_resource(ProviderProfileAPI, '/profile')
