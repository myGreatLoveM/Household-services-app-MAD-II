import time
from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from application.extensions import db, ma, cache
from .models import User, Profile
from application.admin.models import Category
from application.providers.models import Provider, Service
from application.customers.models import Booking, Review
from application.admin.schemas import CategorySchema
from application.providers.schemas import ProviderSchema, ServiceSchema
from application.utils import success_response, error_response
from application.enums import BookingStatusEnum
from application.utils import make_cache_key



class CategoryExploreListAPI(Resource):

    @cache.cached(timeout=300, key_prefix=make_cache_key)
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

    @cache.cached(timeout=300, key_prefix=make_cache_key)
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
        

class ActiveServiceListAPI(Resource):

    @cache.cached(timeout=3000, key_prefix=make_cache_key)
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config.get('ITEMS_PER_PAGE', 10)
        search_query = request.args.get('query')

        try:
            paginated = (
                db.session.query(
                    Service,
                    db.func.count(
                        db.case(
                            (Booking.status.notin_([BookingStatusEnum.PENDING.value, BookingStatusEnum.REJECT.value, BookingStatusEnum.CONFIRM.value]), Booking.id)
                        )
                    ).label('total_bookings'),
                    db.func.count(
                        Review.id
                    ).label('total_reviews'),
                    db.func.coalesce(
                        db.func.avg(Review.rating), 0
                    ).label('avg_rating')
                )
                .outerjoin(Provider, Service.provider)
                .outerjoin(Booking, Service.bookings)
                .outerjoin(Review, Booking.review)
                .filter(
                    Provider.is_approved.is_(True),
                    Provider.is_blocked.is_(False), 
                    Service.is_approved.is_(True),
                    Service.is_blocked.is_(False), 
                    Service.is_active.is_(True)
                )
                .group_by(Service.id)
                .paginate(page=page, per_page=per_page, error_out=False)
            )
            
            schema = ServiceSchema()
            services = []

            for service_obj, total_bookings, total_reviews, avg_rating in paginated:
                service = schema.dump(service_obj)
                service['total_bookings'] = total_bookings
                service['total_reviews'] = total_reviews
                service['avg_rating'] = avg_rating

                services.append(service)

            data = {
                'no_of_services': paginated.total,
                'no_of_pages': paginated.pages,
                'current_page': paginated.page,
                'per_page': per_page,
                'services': services
            }
            return success_response(data=data)
        except SQLAlchemyError as e:
            return error_response('Something went wrong while fetching services')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')


class ActiveServiceAPI(Resource):

    @cache.cached(timeout=1000, key_prefix=make_cache_key)
    def get(self, service_id):
        print('slnblkfnb')
        try:
            service = (
                db.session.query(
                    Service,
                )
                .outerjoin(Provider, Service.provider)
                .filter(
                    Service.id.is_(service_id),
                    Provider.is_approved.is_(True),
                    Provider.is_blocked.is_(False), 
                    Service.is_approved.is_(True),
                    Service.is_blocked.is_(False), 
                    Service.is_active.is_(True)
                )
                .first()
            )

            if not service:
                return error_response(f'Service not exist with {service_id}', status_code=400)

            service_schema = ServiceSchema()
            service = service_schema.dump(service)

            return success_response(data={'service': service})
        except SQLAlchemyError as e:
            return error_response('Something went wrong while fetching service')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')



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


# @core.route('/main/providers/<int:prov_id>')
# def get_verified_provider(prov_id):
    # try:
    #     provider, profile = (
    #         db.session.query(
    #             Provider,
    #             Profile,
    #         )
    #         .join(User, Provider.user)
    #         .join(Profile, User.profile)
    #         .filter(
    #             Provider.id==prov_id, Provider.is_approved==True, Provider.is_blocked==False
    #         )
    #         .first()
    #     )
    #     if provider is None:
    #         raise NotFound('Provider not found')
        
    # except SQLAlchemyError as e:
    #     print(e)
    #     raise InternalServerError()
    # return render_template('core/provider_profile.html', provider=provider, profile=profile)