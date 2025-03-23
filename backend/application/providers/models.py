from datetime import datetime
from application.enums import ProviderAvailabilityEnum
from application.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property


class Provider(db.Model):
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True)
    is_approved = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk__providers__users__user_id'), unique=True, nullable=False,)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', name='fk__providers__categories__category_id'), nullable=False)
    experience = db.Column(db.Integer, default=0)
    wallet = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    approved_at = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'category_id',  name='uq__providers__user_id__category_id'),
    )

    user = db.relationship('User', back_populates='provider')
    category = db.relationship('Category', back_populates='providers')  
    services = db.relationship('Service', back_populates='provider', lazy='dynamic')


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    is_approved = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    prov_id = db.Column(db.Integer, db.ForeignKey('providers.id', name='fk__services__providers__prov_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    time_required_hr = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.String(50), default=ProviderAvailabilityEnum.ALL_TIME.value)  # e.g., 'Weekdays', 'Weekends', '24/7'
    description = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    approved_at = db.Column(db.DateTime)

    provider = db.relationship('Provider', back_populates='services')
    bookings = db.relationship('Booking', back_populates='service', lazy='dynamic')