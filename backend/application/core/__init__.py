from flask import Blueprint
from flask_restful import Api

core = Blueprint('core', __name__)


from .resources import CategoryExploreListAPI, CategoryExploreAPI, ActiveServiceListAPI, ActiveServiceAPI

api = Api(core)

api.add_resource(CategoryExploreListAPI, '/categories')
api.add_resource(CategoryExploreAPI, '/categories/<int:cat_id>')


api.add_resource(ActiveServiceListAPI, '/active-services')
api.add_resource(ActiveServiceAPI, '/active-services/<int:service_id>')

