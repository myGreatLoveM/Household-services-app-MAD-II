from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from application.extensions import db
from .models import Admin, Category
from application.customers.models import Booking, Customer, Payment
from application.providers.models import Provider, Service

from .schemas import CategorySchema
from .parsers import admin_provider_query_args_parser
from application.providers.schemas import ProviderSchema

from application.enums import BookingStatusEnum, UserRoleEnum, UserStatusEnum, PaymentStatusEnum
from application.utils import error_response, success_response
from application.decorators import role_required



class AdminCategoryListAPI(Resource):

    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def get(self):
        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config.get('ITEMS_PER_PAGE', 6)

        try:
            paginated_data = (
                db.session.query(
                    Category,
                    db.func.coalesce(
                        db.func.count(
                            db.distinct(
                                db.case((db.and_(Provider.is_approved==True, Provider.is_blocked==False), Provider.id))
                            )
                        ), 0
                    ).label('active_providers'),
                    db.func.coalesce(
                        db.func.count(
                            db.distinct(
                                db.case((db.and_(Service.is_approved==True, Service.is_blocked==False, Service.is_active==True, Provider.is_approved==True, Provider.is_blocked==False), Service.id))
                            )
                        ), 0
                    ).label('active_services'),
                    db.func.coalesce(
                        db.func.count(
                            db.distinct(
                                db.case((Booking.status.in_([BookingStatusEnum.ACTIVE.value, BookingStatusEnum.COMPLETE.value]), Booking.id))
                            )
                        ), 0
                    ).label('total_bookings'),
                )
                .outerjoin(Provider, Category.providers)
                .outerjoin(Service, Provider.services)
                .outerjoin(Booking, Service.bookings)
                .group_by(Category.id)
                .paginate(page=page, per_page=per_page, error_out=False)
            )
            
            schema = CategorySchema(exclude=['providers', 'short_description', 'long_description'])
            categories = []
            
            for category_obj, active_providers, active_services, total_bookings in paginated_data:
                category = schema.dump(category_obj)
                category['active_providers'] = active_providers
                category['active_services'] = active_services
                category['total_bookings'] = total_bookings
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
            print(e)
            return error_response('Somthing went wrong, please try again..')

    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def post(self):
        data = request.get_json()
        print(data)
        return {}

class AdminCategoryAPI(Resource):

    def get(self, cat_id):
        try:
            schema = CategorySchema(exclude=[''])
        except SQLAlchemyError as e:
            return error_response('Something went wrong while fetching categories')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')



class AdminServiceListAPI(Resource):

    def get(self):
        pass


class AdminServiceAPI(Resource):

    def get(self, service_id):
        pass

    def put(self, service_id):
        pass


class AdminProviderListAPI(Resource):

    def get(self):
        parsed_req_args = admin_provider_query_args_parser.parse_args()
        page = parsed_req_args.get('page')
        status = parsed_req_args.get('status')
        per_page = current_app.config.get('ITEMS_PER_PAGE', 6)

        schema = ProviderSchema(exclude=['services'])
        providers = []

        try:
            if status == UserStatusEnum.NOT_APPROVED.value:
                paginated_data = (
                    Provider.query.filter(Provider.is_approved.is_(False)).paginate(page=page, per_page=per_page, error_out=False)
                )

                for provider_data in paginated_data:
                    provider = schema.dump(provider_data)
                    provider['category'] = provider.get('category').get('name')
                    providers.append(provider)
            
            else:
                paginated_data = (
                    db.session.query(
                        Provider,
                        db.func.count(
                            db.case(
                                (db.and_(Service.is_approved==True, Service.is_blocked==False, Service.is_active==True), Service.id)
                            )
                        ).label('active_services'),
                        db.func.count(
                            db.case(
                                (Booking.status.in_([BookingStatusEnum.ACTIVE.value, BookingStatusEnum.COMPLETE.value]), Booking.id)
                            )
                        ).label('active_bookings')
                    )
                    .filter(Provider.is_approved.is_(True)) 
                    .outerjoin(Service, Provider.services)
                    .outerjoin(Booking, Service.bookings)
                    .group_by(Provider.id)
                    .order_by(Provider.id)
                    .paginate(page=page, per_page=per_page, error_out=False)
                )

                for provider_data, active_services, active_bookings in paginated_data:
                    provider = schema.dump(provider_data)
                    provider['category'] = provider.get('category').get('name')
                    provider['active_services'] = active_services
                    provider['active_bookings'] = active_bookings
                    providers.append(provider)

            data = {
                'no_of_providers': paginated_data.total,
                'no_of_pages': paginated_data.pages,
                'current_page': paginated_data.page,
                'per_page': paginated_data.per_page,
                'providers': providers
            }

            return success_response(data=data)
        except SQLAlchemyError as e:
            return error_response('Something went wrong while fetching providers')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')


class AdminProviderAPI(Resource):

    def get(self, prov_id):
        pass

    def put(self, prov_id):
        pass


class AdminCustomerListAPI(Resource):

    def get(self):
        page = request.args.get('page', default=1, type=int)
        per_page = current_app.config.get('ITEMS_PER_PAGE', 6)

        try:
            paginated_data = (
                db.session.query(
                    Customer,
                    db.func.count(
                        db.case(
                            (Booking.status.is_(BookingStatusEnum.ACTIVE.value), Booking.id)
                        )
                    ).label('active_bookings'),
                    db.func.count(
                        db.case(
                            (Booking.status.in_([BookingStatusEnum.ACTIVE.value, BookingStatusEnum.COMPLETE.value, BookingStatusEnum.CLOSE.value]), Booking.id)
                        )
                    ).label('total_bookings'),
                    db.func.coalesce(
                        db.func.sum(
                            db.case(
                                (Payment.status.is_(PaymentStatusEnum.PAID.value), Payment.total_amount)
                            )
                        ), 0
                    )
                    .label('lifetime_spent'),
                )
                .outerjoin(Booking, Customer.bookings)
                .outerjoin(Payment, Booking.payment)
                .group_by(Customer.id)
                .order_by(Customer.id)
                .paginate(page=page, per_page=per_page, error_out=False)
            )



            return {}
        except SQLAlchemyError as e:
            return error_response('Something went wrong while fetching customers')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')

class AdminCustomerAPI(Resource):

    def get(self, cust_id):
        pass

    def put(self, cust_id):
        pass
