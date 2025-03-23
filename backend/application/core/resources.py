import time
from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from application.extensions import db, ma
from application.admin.models import Category
from application.providers.models import Provider, Service
from application.admin.schemas import CategorySchema
from application.utils import success_response, error_response


class CategoryExploreListAPI(Resource):

    def get(self):
        try:
            page = request.args.get('page', default=1, type=int)
            per_page = current_app.config.get('ITEMS_PER_PAGE', 6)
            only_names = request.args.get('only_names', default=False)

            if only_names:
                cat_names = db.session.query(Category.name).all()
                cat_names = list(map(lambda c: c[0], cat_names))
                
                return success_response(data={'categories': cat_names})

            active_provs_with_active_services_subq = (
                db.session.query(
                    Provider, 
                    db.func.count(
                        db.case(
                            (db.and_(Service.is_blocked.is_(False), Service.is_approved.is_(True), Service.is_active.is_(True)), Service.id)
                        )
                    ).label('active_services')
                )
                .outerjoin(Service, Provider.services)
                .filter(Provider.is_blocked.is_(False), Provider.is_approved.is_(True))
                .group_by(Provider.id)
                .subquery() 
            )

            paginated_data = (
                db.session.query(
                    Category, 
                    db.func.count(
                        active_provs_with_active_services_subq.c.id
                    ).label('active_provs'), 
                    db.func.coalesce(
                        db.func.sum(
                            active_provs_with_active_services_subq.c.active_services
                        ), 0
                    ).label('active_services')
                )
                .outerjoin(active_provs_with_active_services_subq)
                .group_by(Category.id)
                .paginate(page=page, per_page=per_page, error_out=False)
            )

            schema = CategorySchema(exclude=['providers'])
            categories = []

            for category_obj, active_providers, active_services in paginated_data:
                category = schema.dump(category_obj)
                category['active_providers'] = active_providers
                category['active_services'] = active_services
                categories.append(category)

            data = {
                'no_of_categories': paginated_data.total,
                'no_of_pages': paginated_data.pages,
                'current_page': paginated_data.page,
                'per_page': per_page,
                'categories': categories
            }

            return success_response(data=data)
        
        except SQLAlchemyError as e:
            return error_response('Something went wrong while fetching categories')
        except Exception as e:
            return error_response('Somthing went wrong, please try again..')
    

class CategoryExploreAPI(Resource):

    def get(self, cat_id):
        try:
            category_obj = Category.query.filter(Category.id.is_(cat_id)).first()

            if not category_obj:
                return error_response(f'No such category exits with {cat_id} id', is_restful=True, status_code=404)
              
            schema = CategorySchema()
            category = schema.dump(category_obj)
            return success_response(data=category)
        except SQLAlchemyError as e:
            return error_response('Something went wrong while fetching category')
        except Exception as e:
            return error_response('Somthing went wrong, please try again..')
        

# class ListedServicesListAPI(Resource):

#     def get(self):
#         cat_id = request.args.get('cat_id', None, type=int)
#         page = request.args.get('page', 1, type=int)
#         per_page = current_app.config.get('ITEMS_PER_PAGE', 10)


# @core.route('/main/services', methods=['GET', 'POST'])
# def get_all_listed_services():
#     cat_id = request.args.get('cat_id', None, type=int)
#     page = request.args.get('page', 1, type=int)
#     per_page = current_app.config.get('ITEMS_PER_PAGE', 10)

#     try:
#         categories = Category.query.all()

#         active_services_q = (
#             db.session.query(
#                 Service, Provider, Profile
#             )
#             .outerjoin(Provider, Service.provider)
#             .outerjoin(Category, Provider.category)
#             .join(User, Provider.user)
#             .join(Profile, User.profile)
#             .filter(
#                 Provider.is_approved.is_(True),
#                 Provider.is_blocked.is_(False), 
#                 Service.is_approved.is_(True),
#                 Service.is_blocked.is_(False), 
#                 Service.is_active.is_(True)
#             )
#         )

#         if cat_id:
#             active_services_q = (
#                 active_services_q
#                 .join(Category, Provider.category)
#                 .filter(Category.id.is_(cat_id))
#             )

#         if request.method == 'POST':
#             selected_categories = request.form.getlist('category', None)
#             min_price = request.form.get('min_price', type=int)
#             max_price = request.form.get('max_price', type=int)
    
#             search_by = request.form.get('search_by', None)

#             if selected_categories:
#                 active_services_q = active_services_q.join(Category, Provider.category).filter(Category.name.in_(selected_categories))

#             if min_price is not None:
#                 active_services_q = active_services_q.filter(Service.price >= min_price)
#             if max_price is not None:
#                 active_services_q = active_services_q.filter(Service.price <= max_price)

#             if search_by is not None:
#                 active_services_q = active_services_q.filter(
#                     User.username.like(f'%{search_by}%') | 
#                     Profile.location.like(f'%{search_by}%') | 
#                     Profile.full_name.like(f'%{search_by}%') |
#                     Service.title.like(f'%{search_by}%') |
#                     Category.name.like(f'%{search_by}%') 
#                 )

#         services = active_services_q.paginate(page=page, per_page=per_page, error_out=False)
#     except SQLAlchemyError as e:
#         raise InternalServerError()
#     return render_template('core/all_services.html', services=services, categories=categories)


# @core.route('/main/services/<int:service_id>')
# def get_listed_service(service_id):
#     form = BookingForm()
#     try:
#         service, provider = (
#             db.session.query(
#                 Service,
#                 Provider
#             )
#             .join(Provider, Service.provider)
#             .filter(
#                 Service.id == service_id, Service.is_approved == True, Service.is_blocked == False, Service.is_active == True
#             )
#             .first()
#         )
#         if service is None:
#             raise NotFound('Service not found')
#     except SQLAlchemyError as e:
#         raise InternalServerError()
#     return render_template('core/single_service.html', service=service, provider=provider, form=form)   