from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
import time
from datetime import datetime
from application.extensions import db
from .models import Admin, Category
from application.customers.models import Booking, Customer, Payment
from application.providers.models import Provider, Service

from .schemas import CategorySchema, CreateCategorySchema
from .parsers import admin_provider_query_args_parser, admin_service_query_args_parser
from application.providers.schemas import ProviderSchema, ServiceSchema

from application.enums import BookingStatusEnum, ProviderServiceStatusEnum, UserRoleEnum, UserStatusEnum, PaymentStatusEnum
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
                .order_by(Category.created_at.desc())
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
        try:
            schema = CreateCategorySchema()
            val_data = schema.load(data)
            admin = Admin.query.first()

            name = val_data.get('name')
            base_price = val_data.get('basePrice')
            min_time_hr = val_data.get('minTime')
            service_rate = val_data.get('serviceRate')
            booking_rate = val_data.get('bookingRate')
            transaction_rate = val_data.get('transactionRate')
            short_description = val_data.get('description')

            is_cat_exist_with_name = Category.query.filter_by(name=name).first()

            if is_cat_exist_with_name:
                return error_response('Category with name already exists!!', status_code=409)

            new_category = Category(
                name=name, 
                base_price=base_price, 
                min_time_hr=min_time_hr,
                commission_rate=service_rate, 
                booking_rate=booking_rate, 
                transaction_rate=transaction_rate, short_description=short_description 
            )

            admin.categories.append(new_category)
            db.session.add(new_category)
            db.session.commit()
            time.sleep(5)
            return success_response(status_code=201)
        except ValidationError as e:
            print(e)
            return error_response('validation errors', errors=e.messages, status_code=400)
        except SQLAlchemyError as e:
            return error_response('Something went wrong while creating new category!!')
        except Exception as e:
            print(e)
            db.session.rollback()
            return error_response('Somthing went wrong, please try again..')


class AdminCategoryAPI(Resource):
    
    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def get(self, cat_id):
        try:
            category, *stats = (
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
                                db.case((db.and_(Service.is_approved==True, Service.is_blocked==False, Service.is_active, Provider.is_approved==True, Provider.is_blocked==False), Service.id))
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
                    db.func.coalesce(
                        db.func.sum(
                            db.case((Payment.status.is_(PaymentStatusEnum.PAID.value), Payment.final_admin_amount))
                        ), 0
                    ).label('total_revenue'),  
                )
                .outerjoin(Provider, Category.providers)
                .outerjoin(Service, Provider.services)
                .outerjoin(Booking, Service.bookings)
                .outerjoin(Payment, Booking.payment)
                .group_by(Category.id)
                .filter(Category.id == cat_id)
                .first()
            )

            if not category:
                return error_response(f'Category not exist with id {cat_id}', status_code=400)

            schema = CategorySchema(exclude=['providers'])
            category = schema.dump(category)
            category['active_providers'] = stats[0]
            category['active_services'] = stats[1]
            category['total_bookings'] = stats[2]
            category['total_revenue'] = stats[3]

            return success_response(data={'category': category})
           
        except SQLAlchemyError as e:
            return error_response('Something went wrong while fetching category')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')

    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def put(self, cat_id):
        try:
            category = Category.query.filter_by(id=cat_id).first()
            
            if not category:
                return error_response(f'Category not exists with id {cat_id}', status_code=400)

            data = request.get_json()
            
            schema = CreateCategorySchema()
            val_data = schema.load(data)

            name = val_data.get('name')
            base_price = val_data.get('basePrice')
            min_time_hr = val_data.get('minTime')
            service_rate = val_data.get('serviceRate')
            booking_rate = val_data.get('bookingRate')
            transaction_rate = val_data.get('transactionRate')
            short_description = val_data.get('description')

            is_cat_exist_with_name = Category.query.filter_by(name=name).first()

            if is_cat_exist_with_name and is_cat_exist_with_name != category.name :
                return error_response('Category with name already exists!!', status_code=409)

            category.name = name 
            category.base_price = base_price 
            category.min_time_hr = min_time_hr
            category.commission_rate = service_rate 
            category.booking_rate = booking_rate 
            category.transaction_rate = transaction_rate 
            category.short_description = short_description 

            db.session.commit()
            time.sleep(5)
            return success_response(status_code=204)
        except ValidationError as err:
            return error_response('validation errors', errors=err.messages, status_code=400)
        except SQLAlchemyError as e:
            print(e)
            return error_response('Something went wrong while updating category!!')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')


class AdminServiceListAPI(Resource):

    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def get(self):
        parsed_req_args = admin_service_query_args_parser.parse_args()
        page = parsed_req_args.get('page')
        status = parsed_req_args.get('status')
        per_page = current_app.config.get('ITEMS_PER_PAGE', 6)

        try:
            query = db.session.query(Service)

            if status == ProviderServiceStatusEnum.APPROVE.value:
                query = query.filter(Service.is_approved == True)

            elif status == ProviderServiceStatusEnum.PENDING.value:
                query = query.filter(Service.is_approved == False)

            paginated_data = query.order_by(Service.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )

            schema = ServiceSchema(exclude=[])
            services = schema.dump(paginated_data.items, many=True)

            data = {
                "no_of_services": paginated_data.total,
                'no_of_pages': paginated_data.pages,
                'current_page': paginated_data.page,
                'per_page': per_page,
                'services': services
            }

            return success_response(data=data)

        except SQLAlchemyError as e:
            return error_response('Something went wrong while fetching services')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')


class AdminServiceMgmtAPI(Resource):
    
    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def get(self, service_id):
        pass
    
    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def patch(self, service_id):
        try:
            service = Service.query.filter_by(id=service_id).first()

            if not service:
                return error_response(f'Service not exist with id {service_id}', status_code=404)

            if not service.is_approved and not service.is_blocked and not service.approved_at:
                service.is_approved = True
                service.is_active = True
                service.approved_at = datetime.now()
            
            elif service.is_blocked:
                service.is_blocked = False

            db.session.commit()
            return success_response(status_code=204)
        except SQLAlchemyError as e:
            return error_response('Something went wrong while updating status of service!!')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')

    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def delete(self, service_id):
        try:
            service = Service.query.filter_by(id=service_id).first()

            if not service:
                return error_response(f'Service not exist with id {service_id}', status_code=404)
            
            if not service.is_blocked:
                service.is_blocked = True

            db.session.commit()
            
            return success_response(status_code=204)
        except SQLAlchemyError as e:
            return error_response('Something went wrong while blocking service!!')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')
    

class AdminProviderListAPI(Resource):

    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def get(self):
        parsed_req_args = admin_provider_query_args_parser.parse_args()
        page = parsed_req_args.get('page')
        status = parsed_req_args.get('status')
        per_page = current_app.config.get('ITEMS_PER_PAGE', 6)

        schema = ProviderSchema(exclude=['services'])
        providers = []

        try:
            if status == UserStatusEnum.PENDING.value:
                paginated_data = (
                    Provider.query.filter(Provider.is_approved.is_(False)).paginate(page=page, per_page=per_page, error_out=False)
                )

                for provider_data in paginated_data:
                    provider = schema.dump(provider_data)
                    provider['category'] = provider.get('category').get('name')
                    providers.append(provider)
            
            elif status == UserStatusEnum.APPROVE.value:
                paginated_data = (
                    db.session.query(
                        Provider,
                        db.func.count(
                            db.distinct(
                                db.case(
                                    (db.and_(Service.is_approved==True, Service.is_blocked==False, Service.is_active==True), Service.id)
                                )
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
                    .order_by(Provider.id.desc())
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


class AdminProviderMgmtAPI(Resource):
    
    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def get(self, prov_id):
        pass
    
    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def patch(self, prov_id):
        try:
            provider = Provider.query.filter_by(id=prov_id).first()

            if not provider:
                return error_response(f'Provider not exist with {prov_id}', status_code=404)
            
            if not provider.is_approved and not provider.is_blocked and not provider.approved_at: 
                provider.is_approved = True
                provider.approved_at = datetime.now()

            elif provider.is_blocked:
                provider.is_blocked = False

            db.session.commit()
            return success_response(status_code=204)
        except SQLAlchemyError as e:
            return error_response('Something went wrong while updating status of provider!!')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')

    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def delete(self, prov_id):
        try:
            provider = Provider.query.filter_by(id=prov_id).first()

            if not provider:
                return error_response(f'Provider not exist with {prov_id}', status_code=404)
            
            if not provider.is_blocked:
                provider.is_blocked = True

            db.session.commit()
            return success_response(status_code=204)
        except SQLAlchemyError as e:
            return error_response('Something went wrong while blocking provider!!')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')


class AdminCustomerListAPI(Resource):

    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
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


class AdminCustomerMgmtAPI(Resource):

    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def get(self, cust_id):
        pass
    

    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def patch(self, cust_id):
        try:
            customer = Customer.query.filter_by(id=cust_id).first()

            if not customer:
                return error_response(f'Customer not exist with {cust_id}', status_code=400)
            
            if customer.is_blocked: 
                customer.is_blocked = False
                db.session.commit()

            return success_response(status_code=204)
        except SQLAlchemyError as e:
            return error_response('Something went wrong while updating status of customer!!')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')


    @jwt_required()
    @role_required(UserRoleEnum.ADMIN.value)
    def delete(self, cust_id):
        try:
            customer = Customer.query.filter_by(id=cust_id).first()

            if not customer:
                return error_response(f'Customer not exist with {cust_id}', status_code=400)
            
            if not customer.is_blocked: 
                customer.is_blocked = True
                db.session.commit()

            return success_response(status_code=204)
        except SQLAlchemyError as e:
            return error_response('Something went wrong while updating status of customer!!')
        except Exception as e:
            print(e)
            return error_response('Somthing went wrong, please try again..')
