from . import admin
from .models import Category
from application.extensions import db
from application.utils import success_response, error_response



@admin.route('/categories/list')
def get_list_of_all_categories():
    try:
        raw_data = db.session.query(Category.name).all()
        categories = [cat[0] for cat in raw_data]
    except Exception as e:
        return error_response('', status_code=500)

    return success_response({"no_of_categories":len(categories) ,"categories": categories}, status_code=200)