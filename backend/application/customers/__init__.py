from flask import Blueprint
from flask_restful import Api

customer = Blueprint('customer', __name__)


from .resources import BookAPI

api = Api(customer)

api.add_resource(BookAPI, "/bookings")