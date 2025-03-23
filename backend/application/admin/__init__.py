from flask import Blueprint
from flask_restful import Api

admin = Blueprint('admin', __name__)


from .views import *
from .resources import AdminCategoryListAPI, AdminCategoryAPI, AdminServiceListAPI, AdminServiceAPI, AdminProviderListAPI, AdminProviderAPI, AdminCustomerAPI, AdminCustomerListAPI


api = Api(admin)

api.add_resource(AdminCategoryListAPI, '/categories')
api.add_resource(AdminCategoryAPI, '/categories/<int:cat_id>')

api.add_resource(AdminServiceListAPI, '/services')
api.add_resource(AdminServiceAPI, '/services/<int:service_id>')

api.add_resource(AdminProviderListAPI, '/providers')
api.add_resource(AdminProviderAPI, '/providers/<int:prov_id>')

api.add_resource(AdminCustomerListAPI, '/customers')
api.add_resource(AdminCustomerAPI, '/customers/<int:cust_id>')