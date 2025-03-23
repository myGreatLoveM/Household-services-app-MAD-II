from flask import Blueprint
from application.core import core as core_blueprint
from application.auth import auth as auth_blueprint
from application.admin import admin as admin_blueprint
from application.customers import customer as customer_blueprint
from application.providers import provider as provider_blueprint


def create_all_api_resource_blueprint(main_filename: str) -> Blueprint:
    api_resources_bp = Blueprint('api_resources_bp', main_filename)

    api_resources_bp.register_blueprint(core_blueprint, url_prefix='/')

    api_resources_bp.register_blueprint(admin_blueprint, url_prefix='/admin')

    api_resources_bp.register_blueprint(provider_blueprint, url_prefix='/providers/<int:prov_id>')

    api_resources_bp.register_blueprint(customer_blueprint, url_prefix='/customers/<int:cust_id>')

    api_resources_bp.register_blueprint(auth_blueprint, url_prefix='/auth')

    return api_resources_bp

