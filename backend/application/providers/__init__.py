from flask import Blueprint
from flask_restful import Api

provider = Blueprint('provider', __name__)

api = Api(provider)

from .resources import ProviderServiceListAPI, ProviderProfileAPI, ProviderServiceMgmtAPI, ProviderBookingListAPI, ProviderBookingMgmtAPI, ProviderClosedBookingCSVExport, ProviderClosedBookingTask

api.add_resource(ProviderServiceListAPI, '/services')

api.add_resource(ProviderServiceMgmtAPI, '/services/<int:service_id>')

api.add_resource(ProviderBookingListAPI, '/bookings')

api.add_resource(ProviderBookingMgmtAPI, '/bookings/<int:booking_id>')

api.add_resource(ProviderClosedBookingCSVExport, '/bookings/csv-export')

api.add_resource(ProviderClosedBookingTask, '/bookings/csv-export/<task_id>')

api.add_resource(ProviderProfileAPI, '/profile')
