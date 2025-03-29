from marshmallow import Schema, ValidationError, fields, validate, validates, pre_load
from application.extensions import ma
from .models import Customer, Booking, Payment, Review



class CustomerSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Customer
        load_instance = True
        include_relationships = False
        include_fk = False

    user = fields.Nested('UserSchema', dump_only=True, only=['username', 'email', 'profile'])
    bookings = fields.List(fields.Nested('BookingSchema', many=True, exclude=['customer', 'payment', 'review']))


class BookingSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Booking
        load_instance = True
        include_relationships = False
        include_fk = False

    customer = fields.Nested('CustomerSchema', dump_only=True, exclude=['bookings'])
    payment = fields.Nested('PaymentSchema', dump_only=True, exclude=['booking'])
    review = fields.Nested('ReviewSchema', dump_only=True)


class PaymentSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Payment
        load_instance = True
        include_relationships = False
        include_fk = False

    booking = fields.Nested('BookingSchema', dump_only=True, exclude=['payment', 'review'])


class ReviewSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Review
        load_instance = True
        include_relationships = False
        include_fk = False
