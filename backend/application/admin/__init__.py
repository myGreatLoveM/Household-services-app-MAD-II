from flask import Blueprint
from flask_restful import Api

admin = Blueprint('admin', __name__)


from .resources import AdminCategoryListAPI, AdminCategoryAPI, AdminServiceListAPI, AdminServiceMgmtAPI, AdminProviderListAPI, AdminProviderMgmtAPI, AdminCustomerMgmtAPI, AdminCustomerListAPI, AdminPaymentsListAPI


api = Api(admin)

api.add_resource(AdminCategoryListAPI, '/categories')
api.add_resource(AdminCategoryAPI, '/categories/<int:cat_id>')

api.add_resource(AdminServiceListAPI, '/services')
api.add_resource(AdminServiceMgmtAPI, '/services/<int:service_id>')

api.add_resource(AdminProviderListAPI, '/providers')
api.add_resource(AdminProviderMgmtAPI, '/providers/<int:prov_id>')

api.add_resource(AdminCustomerListAPI, '/customers')
api.add_resource(AdminCustomerMgmtAPI, '/customers/<int:cust_id>')


api.add_resource(AdminPaymentsListAPI, '/payments')