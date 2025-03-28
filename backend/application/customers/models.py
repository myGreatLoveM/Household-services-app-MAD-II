from datetime import datetime
from application.core.models import Profile, User
from application.enums import BookingStatusEnum, PaymentMethodEnum, PaymentStatusEnum
from application.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    is_blocked = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk__customers__users__user_id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship('User', back_populates='customer')
    bookings = db.relationship('Booking', back_populates='customer', lazy='dynamic')
    payments = db.relationship('Payment', lazy='dynamic')

    __table_args__ = (
        db.UniqueConstraint('user_id', name='uq__customers__user_id'),
    )


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id', name='fk__bookings__customers__cust_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id', name='fk__bookings__services__service_id'), nullable=False)
    status = db.Column(db.String(20), default=BookingStatusEnum.PENDING.value) # 'pending', 'confirmed', 'reject', 'completed'
    is_closed = db.Column(db.Boolean, default=False)
    book_date = db.Column(db.DateTime)
    fullfillment_date = db.Column(db.DateTime)
    confirm_date = db.Column(db.DateTime)
    complete_date = db.Column(db.DateTime)
    closed_date = db.Column(db.DateTime)
    remark = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    customer = db.relationship('Customer', back_populates='bookings')
    service = db.relationship('Service', back_populates='bookings')
    payment = db.relationship('Payment', uselist=False)
    review = db.relationship('Review', uselist=False)


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id', name='fk__payments__customers__cust_id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    status = db.Column(db.String(20), default=PaymentStatusEnum.PENDING.value)  # 'paid', 'pending', 'cancelled'
    amount = db.Column(db.Integer, nullable=False)
    commission_fee = db.Column(db.Integer,  default=0)
    platform_fee = db.Column(db.Integer, default=0)
    transaction_fee = db.Column(db.Integer, default=0)
    discount = db.Column(db.Integer, default=0)
    method = db.Column(db.String(20), default=PaymentMethodEnum.CREDIT_CARD.value) 

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        db.UniqueConstraint('cust_id', 'booking_id', name='uq__payments__cust_id__booking_id'),
    )

    @hybrid_property
    def total_amount(self):
        return self.amount + self.platform_fee + self.transaction_fee - self.discount

    def calculate_final_amount(self):
        return round(self.amount + self.platform_fee + self.transaction_fee - self.discount, 2)

    @hybrid_property
    def final_provider_amount(self):
        return self.amount - self.commission_fee
    
    @hybrid_property
    def final_admin_amount(self):
        return self.commission_fee + self.platform_fee + self.transaction_fee



class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id', name='fk__reviews__customers__cust_id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id', name='fk__reviews__bookings__booking_id'), nullable=False)
    rating = db.Column(db.Integer, default=5)
    comment = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # booking = db.relationship('Booking', back_populates='review')

    __table_args__ = (
        db.UniqueConstraint('cust_id', 'booking_id', name='uq__reviews__cust_id__booking_id'),
        db.CheckConstraint('rating >= 0 AND rating <= 5', name='check_rating_between_0_and_5'),
    )














# class Refund(db.Model):
#     __tablename__ = 'refunds'

#     id = db.Column(db.Integer, primary_key=True)
#     booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
#     transaction_id = db.Column(db.Integer, db.ForeignKey(CustomerPayment.id), nullable=False)
#     amount = db.Column(db.Float, nullable=False)  # Amount to be refunded
#     status = db.Column(db.String(20), default='Pending')  # 'Pending', 'Processed', 'Failed'
#     cancellation_charge = db.Column(db.Integer, default=0) # for customer cancellation
#     penalty = db.Column(db.Integer, default=0) # penalty on provider cancellation
#     created_at = db.Column(db.DateTime, default=datetime.now)
#     updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

#     booking = db.relationship('Booking', back_populates='refund')
