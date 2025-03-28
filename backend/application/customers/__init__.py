from flask import Blueprint
from flask_restful import Api

customer = Blueprint('customer', __name__)


from .resources import CustomerBookingsListAPI, CustomerBookingMgmtAPI, CustomerPaymentHandleAPI, CustomerProfileAPI

api = Api(customer)

api.add_resource(CustomerBookingsListAPI, "/bookings")

api.add_resource(CustomerBookingMgmtAPI, "/bookings/<int:booking_id>")

api.add_resource(CustomerPaymentHandleAPI, "/payments/<int:payment_id>")

api.add_resource(CustomerProfileAPI, "/profile")


