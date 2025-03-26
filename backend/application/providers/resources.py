from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from application.extensions import db
from .models import Service, Provider
from application.admin.models import Category
from application.core.models import User
from application.customers.models import Booking, Review
from .schemas import ProviderSchema, ServiceSchema, CreateServiceSchema
from application.core.schemas import ProfileSchema, UserSchema
from application.decorators import role_required
from application.utils import error_response, success_response
from application.enums import BookingStatusEnum, UserRoleEnum


class ProviderServiceListAPI(Resource):

  @jwt_required()
  @role_required(UserRoleEnum.PROVIDER.value)
  def get(self, prov_id):
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config.get('ITEMS_PER_PAGE', 6)

    try:
        paginated_data = (
            db.session.query(
                Service,
                db.func.coalesce(
                    db.func.count(
                        db.case(
                            (Booking.status.in_([BookingStatusEnum.ACTIVE.value, BookingStatusEnum.COMPLETE.value]), Booking.id)
                        )
                    ), 0
                ).label('active_bookings'),
                db.func.coalesce(
                    db.func.avg(Review.rating), 0
                ).label('avg_rating')
            )
            .filter(Service.prov_id == prov_id)
            .outerjoin(Booking, Service.bookings)
            .outerjoin(Review, Booking.review)
            .group_by(Service.id)
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        
        services = []
        schema = ServiceSchema()
        for service_obj, active_bookings, avg_rating in paginated_data:
            service = schema.dump(service_obj)
            service['active_bookings'] = active_bookings
            service['avg_rating'] = avg_rating
            services.append(service)

        data = {
            'no_of_services': paginated_data.total,
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
        return error_response('Something went wrong, please try again..')


  @jwt_required()
  @role_required(UserRoleEnum.PROVIDER.value)
  def post(self, prov_id):
    try:
        data = request.get_json()
        schema = CreateServiceSchema()
        val_data = schema.load(data)
        
        name = val_data.get('name')
        price = val_data.get('price')
        time = val_data.get('time')
        description = val_data.get('description')

        is_service_exist_with_name = Service.query.filter_by(name=name, prov_id=prov_id).first()

        if is_service_exist_with_name:
            return error_response('Service with name already exists', status_code=409)
        
        category_name, base_price = (
            db.session.query(Category.name, Category.base_price)
            .filter(Provider.id==prov_id)
            .outerjoin(Category, Provider.category)
            .first()
        )

        if price < base_price:
            return error_response(f'Price should be above base price {base_price} for {category_name}!!')

        new_service = Service(
            name=name,
            price=price,
            time_required_hr=time,
            description=description,
            prov_id=prov_id
        )
        db.session.add(new_service)
        db.session.commit()

        return success_response(status_code=201)
    except ValidationError as err:
      return error_response('validation errors', errors=err.messages, status_code=400)
    except SQLAlchemyError as e:
      db.session.rollback()
      return error_response('Something went wrong while creating new service!!')
    except Exception as e:
      print(e)
      db.session.rollback()
      return error_response('Something went wrong, please try again..')


class ProviderProfileAPI(Resource):
    
  @jwt_required()
  @role_required(UserRoleEnum.PROVIDER.value)
  def get(self, prov_id):
    try:
      provider = (
        db.session.query(
          Provider
        )
        .options(
          db.joinedload(Provider.user).joinedload(User.profile)
        )
        .filter(Provider.id == prov_id)
        .first()
      )

      if not provider:
        return error_response(f'Provider does not exist with id {prov_id}', status_code=404)

      schema = ProviderSchema(exclude=['services'])

      data = {'provider': schema.dump(provider)}
      return success_response(data=data)
      
    except SQLAlchemyError as e:
        return error_response('Something went wrong while creating new service!!')
    except Exception as e:
      print(e)
      return error_response('Something went wrong, please try again..')

  @jwt_required()
  @role_required(UserRoleEnum.PROVIDER.value)
  def put(self, prov_id):
    try:
      data = request.get_json()
      first_name = data.get('firstName')
      last_name = data.get('lastName')
      contact = data.get('contact')
      location = data.get('location')
      bio = data.get('bio')

      provider = Provider.query.filter_by(id=prov_id).first()

      if not provider:
        return error_response(f'Provider not exist with id {prov_id}', status_code=404)

      profile = provider.user.profile
      profile.first_name = first_name
      profile.last_name = last_name
      profile.contact = contact
      profile.location = location
      profile.bio = bio

      db.session.commit()
      return success_response(status_code=201)
    except SQLAlchemyError as e:
      db.session.rollback()
      return error_response('Something went wrong while updating profile!!')
    except Exception as e:
      print(e)
      db.session.rollback()
      return error_response('Something went wrong, please try again..')


class ProviderServiceMgmtAPI(Resource):
   
  @jwt_required()
  @role_required(UserRoleEnum.PROVIDER.value)
  def patch(self, prov_id, service_id):
    try:
      provider = Provider.query.filter_by(id=prov_id).first()

      if not provider:
        return error_response(f'Provider not exist with {prov_id}', status_code=404)
      
      service = provider.services.filter_by(id=service_id).first()

      if not service:
        return error_response(f'service not exist with {service_id}', status_code=404)
      
      if not service.is_approved:
        return error_response(f'Service is not approved', status_code=400)

      if service.is_approved and service.is_blocked:
        return error_response(f'Service is blocked by admin', status_code=400)

      service.is_active = True
      db.session.commit()
      return success_response(status_code=204)         

    except SQLAlchemyError as e:
      db.session.rollback()
      return error_response('Something went wrong while updating service status!!')
    except Exception as e:
      print(e)
      db.session.rollback()
      return error_response('Something went wrong, please try again..')


  @jwt_required()
  @role_required(UserRoleEnum.PROVIDER.value)
  def delete(self, prov_id, service_id):
    try:
      provider = Provider.query.filter_by(id=prov_id).first()

      if not provider:
        return error_response(f'Provider not exist with {prov_id}', status_code=404)
      
      service = provider.services.filter_by(id=service_id).first()

      if not service:
        return error_response(f'service not exist with {service_id}', status_code=404)
      
      if not service.is_approved:
        return error_response(f'Service is not approved', status_code=400)

      if service.is_approved and service.is_blocked:
        return error_response(f'Service is blocked by admin', status_code=400)

      service.is_active = False
      db.session.commit()
      return success_response(status_code=204)         

    except SQLAlchemyError as e:
      db.session.rollback()
      return error_response('Something went wrong while updating service status!!')
    except Exception as e:
      print(e)
      db.session.rollback()
      return error_response('Something went wrong, please try again..')









# --------------------------------------------------------------------------------------------------------------
    # @hybrid_property
    # def category(self):
    #     return self.provider.category.name
    

    # @hybrid_property
    # def avg_rating(self):
    #     return (
    #         db.session.query(
    #             db.func.coalesce(db.func.avg(Review.rating), 0)
    #         )
    #         .outerjoin(Booking, Service.bookings)
    #         .outerjoin(Review, Booking.review)
    #         .group_by(Service.id)
    #         .filter(Service.id.is_(self.id))
    #         .scalar()
    #     )
    
    # @hybrid_property
    # def no_of_reviews(self):
    #     return (
    #         db.session.query(
    #             db.func.coalesce(
    #                 db.func.count(Review.id), 0
    #             )
    #         )
    #         .outerjoin(Booking, Service.bookings)
    #         .outerjoin(Review, Booking.review)
    #         .group_by(Service.id)
    #         .filter(Service.id.is_(self.id))
    #         .scalar()
    #     )
    
    # @hybrid_property
    # def total_served_bookings(self):
    #     return (
    #         db.session.query(
    #             db.func.count(
    #                 db.case(
    #                     (Booking.status.notin_([BookingStatusEnum.PENDING.value, BookingStatusEnum.REJECT.value, BookingStatusEnum.CONFIRM.value]), Booking.id)
    #                 )
    #             )
    #         )
    #         .outerjoin(Booking, Service.bookings)
    #         .group_by(Service.id)
    #         .filter(Service.id.is_(self.id))
    #         .scalar()
    #     )
    
    # @hybrid_property
    # def total_active_bookings(self):
    #     return (
    #         db.session.query(
    #             db.func.count(
    #                 db.case(
    #                     (Booking.status.in_([BookingStatusEnum.ACTIVE.value, BookingStatusEnum.COMPLETE.value]), Booking.id)
    #                 )
    #             )
    #         )
    #         .outerjoin(Booking, Service.bookings)
    #         .group_by(Service.id)
    #         .filter(Service.id.is_(self.id))
    #         .scalar()
    #     )

    # @hybrid_property
    # def top_review(self):
    #     return (
    #         db.session.query(
    #             Review
    #         )
    #         .outerjoin(Booking, Service.bookings)
    #         .outerjoin(Review, Booking.review)
    #         .group_by(Service.id)
    #         .filter(Service.id.is_(self.id))
    #         .order_by(Review.rating.desc(), Review.created_at.desc())
    #         .first()
    #     )

    # @hybrid_property
    # def lifetime_earning(self):
    #     total_amount, total_service_fee =  (
    #         db.session.query(
    #             db.func.coalesce(
    #                 db.func.sum(
    #                     db.case(
    #                         (Booking.status.in_([BookingStatusEnum.CLOSE.value]), CustomerPayment.amount)
    #                     )
    #             ), 0).label('total_amount'),
    #             db.func.coalesce(
    #                 db.func.sum(
    #                     db.case(
    #                         (Booking.status.in_([BookingStatusEnum.CLOSE.value]), CustomerPayment.service_fee)
    #                     )
    #             ), 0).label('total_service_fee'),
    #         )
    #         .outerjoin(Booking, Service.bookings)
    #         .outerjoin(CustomerPayment, Booking.payment)
    #         .group_by(Service.id)
    #         .filter(Service.id.is_(self.id))
    #         .first()
    #     )
    #     return total_amount - total_service_fee
    

    # @hybrid_property
    # def pending_earning(self):
    #     pending_amount, pending_service_fee =  (
    #         db.session.query(
    #             db.func.coalesce(
    #                 db.func.sum(
    #                     db.case(
    #                         (Booking.status.in_([BookingStatusEnum.ACTIVE.value, BookingStatusEnum.COMPLETE.value]), CustomerPayment.amount)
    #                     )
    #             ), 0).label('pending_amount'),
    #             db.func.coalesce(
    #                 db.func.sum(
    #                     db.case(
    #                         (Booking.status.in_([BookingStatusEnum.ACTIVE.value, BookingStatusEnum.COMPLETE.value]), CustomerPayment.service_fee)
    #                     )
    #             ), 0).label('pending_service_fee'),
    #         )
    #         .outerjoin(Booking, Service.bookings)
    #         .outerjoin(CustomerPayment, Booking.payment)
    #         .group_by(Service.id)
    #         .filter(Service.id.is_(self.id))
    #         .first()
    #     )
    #     return pending_amount - pending_service_fee