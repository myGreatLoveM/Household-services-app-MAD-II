from flask import Blueprint


home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    return {'msg': 'ok'}, 200


@home_bp.route('/test')
def test():
    return {'msg': 'ok'}, 200




