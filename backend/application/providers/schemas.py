from marshmallow import fields
from .models import Provider, Service
from application.extensions import ma


class ProviderSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Provider
        load_instance = True
        include_fk = False
        include_relationships = False

    user = fields.Nested('UserSchema', dump_only=True, only=['username'])
    category = fields.Nested('CategorySchema', dump_only=True, only=['name'])
    services = fields.List(fields.Nested('ServiceSchema', many=True, exclude=['provider', 'bookings']))
    location = fields.Method('get_location')

    def get_location(self, obj):
        from application.core.schemas import ProfileSchema
        return ProfileSchema(only=['location']).dump(obj.user.profile)['location']


class ServiceSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Service
        load_instance = True
        include_relationships = False
        include_fk = False









# class Service(db.Model):
#     __tablename__ = 'services'

#     id = db.Column(db.Integer, primary_key=True)
#     is_approved = db.Column(db.Boolean, default=False)
#     is_blocked = db.Column(db.Boolean, default=False)
#     is_active = db.Column(db.Boolean, default=False)
#     prov_id = db.Column(db.Integer, db.ForeignKey('providers.id', name='fk__services__providers__prov_id'), nullable=False)
#     name = db.Column(db.String(50), nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     time_required_hr = db.Column(db.Integer, nullable=False)
#     availability = db.Column(db.String(50), default=ProviderAvailabilityEnum.ALL_TIME.value)  # e.g., 'Weekdays', 'Weekends', '24/7'
#     description = db.Column(db.String(100))

#     created_at = db.Column(db.DateTime, default=datetime.now)
#     updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
#     approved_at = db.Column(db.DateTime)

#     provider = db.relationship('Provider', back_populates='services')
#     bookings = db.relationship('Booking', back_populates='service', lazy='dynamic')