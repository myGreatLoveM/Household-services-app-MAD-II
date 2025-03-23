from flask import Blueprint
from flask_restful import Api

core = Blueprint('core', __name__)


from .resources import CategoryExploreListAPI, CategoryExploreAPI

api = Api(core)

api.add_resource(CategoryExploreListAPI, '/categories')
api.add_resource(CategoryExploreAPI, '/categories/<int:cat_id>')