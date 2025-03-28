from flask import request, current_app
from datetime import datetime
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from application.extensions import db
from application.core.models import User
from .models import Booking, Customer, Payment
from application.providers.models import Service

from .schemas import BookingSchema, CustomerSchema, PaymentSchema
from application.providers.schemas import ServiceSchema
from application.decorators import role_required
from application.utils import success_response, error_response
from application.enums import PaymentMethodEnum, PaymentStatusEnum, UserRoleEnum, BookingStatusEnum

    

class CustomerBookingsListAPI(Resource):
    
  @jwt_required()
  @role_required(UserRoleEnum.CUSTOMER.value)
  def get(self, cust_id):
    try:
      page = request.args.get('page', default=1, type=int)
      per_page = current_app.config.get('ITEMS_PER_PAGE', 6)
      status = request.args.get('status', default=BookingStatusEnum.ACTIVE.value)

      if status not in [BookingStatusEnum.ACTIVE.value, BookingStatusEnum.PENDING.value]:
        return error_response('Invalid status for resource', status_code=400)

      query = (
        db.session.query(
          Booking, 
          Service,
        )
        .outerjoin(Customer, Booking.customer)
        .outerjoin(Service, Booking.service)
      )

      if status == BookingStatusEnum.ACTIVE.value:
        query = query.filter(
          Booking.status.in_([BookingStatusEnum.ACTIVE.value, BookingStatusEnum.COMPLETE.value]), 
          Customer.id==cust_id
        )
      elif status == BookingStatusEnum.PENDING.value:
        query = query.filter(
          Booking.status.notin_([BookingStatusEnum.ACTIVE.value, BookingStatusEnum.COMPLETE.value]), 
          Customer.id==cust_id
        )

      paginated = (
        query
        .order_by(Booking.id.desc())
        .paginate(per_page=per_page, page=page, error_out=False)
      )

      bookings = []
      booking_schema = BookingSchema(exclude=['review'])
      service_schema = ServiceSchema()

      for booking_obj, service_obj in paginated:
        booking = booking_schema.dump(booking_obj)
        booking['service'] = service_schema.dump(service_obj)
        bookings.append(booking)

      data={
        'bookings': bookings,
        'no_of_bookings': paginated.total,
        'no_of_pages': paginated.pages,
        'current_page': paginated.page,
        'per_page': per_page
      }

      return success_response(data=data)
    except SQLAlchemyError as e:
      print(e)
      return error_response('Something went wrong while fetching bookings')
    except Exception as e:
      print(e)
      return error_response('Somthing went wrong, please try again..')


  @jwt_required()
  @role_required(UserRoleEnum.CUSTOMER.value)
  def post(self, cust_id):
    try:
        data = request.get_json()
        book_date = data.get('bookDate')
        fullfillment_date = data.get('fullfillmentDate')
        remark = data.get('remark')
        service_id = int(data.get('serviceId'))

        if not book_date or not fullfillment_date:
            return error_response('Missing required data, dates', status_code=400)

        service = Service.query.filter_by(is_active=True, is_approved=True, is_blocked=False, id=service_id).first()

        if not service:
            return error_response(f'Service not exists with id {service_id}', status_code=400)

        new_booking = Booking(
            cust_id=int(cust_id),
            book_date=datetime.strptime(book_date, "%Y-%m-%d"), 
            fullfillment_date=datetime.strptime(fullfillment_date, "%Y-%m-%d"),
            remark=remark,
        )
        
        service.bookings.append(new_booking)
        db.session.commit()
        return success_response(status_code=201)
    except SQLAlchemyError as e:
      print(e)
      db.session.rollback()
      return error_response('Something went wrong while creating booking')
    except Exception as e:
      print(e)
      db.session.rollback()
      return error_response('Somthing went wrong, please try again..')


class CustomerBookingMgmtAPI(Resource):

  @jwt_required()
  @role_required(UserRoleEnum.CUSTOMER.value)
  def get(self, cust_id, booking_id):
    pass


  @jwt_required()
  @role_required(UserRoleEnum.CUSTOMER.value)
  def patch(self, cust_id, booking_id):
    try:
      booking = (
        db.session.query(
          Booking,
        )
        .outerjoin(Customer, Booking.customer)
        .filter(
          Booking.id == booking_id,
          Customer.id == cust_id
        )
        .first()
      )

      if not booking:
        return error_response(f'Booking not exist with id {booking_id}!!', status_code=400)    
      
      if booking.status ==  BookingStatusEnum.ACTIVE.value:
        booking.status = BookingStatusEnum.COMPLETE.value
        booking.complete_date = datetime.today()
        db.session.commit()
      
      return success_response(status_code=204)
    except SQLAlchemyError as e:
      print(e)
      db.session.rollback()
      return error_response('Something went wrong while booking complete!!')
    except Exception as e:
      print(e)
      db.session.rollback()
      return error_response('Something went wrong, please try again..')



class CustomerPaymentHandleAPI(Resource):

  @jwt_required()
  @role_required(UserRoleEnum.CUSTOMER.value)
  def get(self, cust_id, payment_id):
    try:
      payment = Payment.query.filter_by(id=payment_id, cust_id=cust_id).first()

      if not payment:
        return error_response('Payment is invalid or fraud', status_code=400)

      if payment.status != PaymentStatusEnum.PENDING.value:
        return error_response('Payment is either paid or cancelled', status_code=400)
      
      booking = Booking.query.filter_by(id=payment.booking_id).first()

      if not booking or booking.status != BookingStatusEnum.CONFIRM.value:
        return error_response('Booking is fraud!!!', status_code=400)
      
      payment_schema = PaymentSchema()
      booking_schema = BookingSchema(exclude=['payment', 'review'])

      payment = payment_schema.dump(payment)
      payment['booking'] = booking_schema.dump(booking)

      data = {'payment': payment}
      
      return success_response(data=data)

    except SQLAlchemyError as e:
      print(e)
      return error_response('Something went wrong while fetching payment data')
    except Exception as e:
      print(e)
      return error_response('Somthing went wrong, please try again..')   

  @jwt_required()
  @role_required(UserRoleEnum.CUSTOMER.value)
  def patch(self, cust_id, payment_id):
    try:
      data = request.get_json()
      method = data.get('paymentMethod') 

      payment = Payment.query.filter_by(id=payment_id, cust_id=cust_id).first()

      if not payment:
        return error_response('Payment is invalid or fraud', status_code=400)

      if payment.status != PaymentStatusEnum.PENDING.value:
        return error_response('Payment is either paid or cancelled', status_code=400)


      booking = Booking.query.filter_by(id=payment.booking_id).first()

      if not booking or booking.status != BookingStatusEnum.CONFIRM.value:
        return error_response('Booking is fraud!!!', status_code=400)


      if payment.status == PaymentStatusEnum.PENDING.value:
        payment.status = PaymentStatusEnum.PAID.value
        payment.method = method if method else PaymentMethodEnum.CREDIT_CARD.value
        booking.status = BookingStatusEnum.ACTIVE.value
        db.session.commit()
      
      return success_response(status_code=204)

    except SQLAlchemyError as e:
      print(e)
      db.session.rollback()
      return error_response('Something went wrong during payment accept!!')
    except Exception as e:
      print(e)
      db.session.rollback()
      return error_response('Somthing went wrong, please try again..') 

  @jwt_required()
  @role_required(UserRoleEnum.CUSTOMER.value)
  def delete(self, cust_id, payment_id):
    try:
      payment = Payment.query.filter_by(id=payment_id, cust_id=cust_id).first()

      if not payment:
        return error_response('Payment is invalid or fraud', status_code=400)

      if payment.status != PaymentStatusEnum.PENDING.value:
        return error_response('Payment is either paid or cancelled', status_code=400)

      booking = Booking.query.filter_by(id=payment.booking_id).first()

      if not booking or booking.status != BookingStatusEnum.CONFIRM.value:
        return error_response('Booking is fraud!!!', status_code=400)

      if payment.status == PaymentStatusEnum.PENDING.value:
        payment.status = PaymentStatusEnum.CANCEL.value
        booking.status = BookingStatusEnum.CANCEL.value
        db.session.commit()
      
      return success_response(status_code=204)

    except SQLAlchemyError as e:
      print(e)
      db.session.rollback()
      return error_response('Something went wrong during payment decline!!')
    except Exception as e:
      print(e)
      db.session.rollback()
      return error_response('Somthing went wrong, please try again..')


class CustomerProfileAPI(Resource):
    
  @jwt_required()
  @role_required(UserRoleEnum.CUSTOMER.value)
  def get(self, cust_id):
    try:
      customer = (
        db.session.query(
          Customer
        )
        .options(
          db.joinedload(Customer.user).joinedload(User.profile)
        )
        .filter(Customer.id == cust_id)
        .first()
      )

      if not customer:
        return error_response(f'Customer does not exist with id {cust_id}', status_code=400)

      schema = CustomerSchema(exclude=['bookings'])

      data = {'customer': schema.dump(customer)}
      return success_response(data=data)
      
    except SQLAlchemyError as e:
        return error_response('Something went wrong while fetching profile!!')
    except Exception as e:
      print(e)
      return error_response('Something went wrong, please try again..')

  @jwt_required()
  @role_required(UserRoleEnum.CUSTOMER.value)
  def put(self, cust_id):
    try:
      data = request.get_json()
      first_name = data.get('firstName')
      last_name = data.get('lastName')
      contact = data.get('contact')
      location = data.get('location')
      bio = data.get('bio')

      customer = Customer.query.filter_by(id=cust_id).first()

      if not customer:
        return error_response(f'Provider not exist with id {cust_id}', status_code=404)

      profile = customer.user.profile
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