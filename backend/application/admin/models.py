from datetime import datetime
from application.extensions import db


class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk__admins__users__user_id'), nullable=False)
    wallet = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    categories = db.relationship('Category', lazy='dynamic')

    __table_args__ = (
        db.UniqueConstraint('user_id', name='uq__admins__user_id'),
    )
    

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id', name='fk__categories__admins__admin_id'), nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)
    base_price = db.Column(db.Integer, nullable=False)
    min_time_hr = db.Column(db.Integer, default=1)
    commission_rate = db.Column(db.Integer, nullable=False)
    booking_rate = db.Column(db.Integer, nullable=False)
    transaction_rate = db.Column(db.Integer, nullable=False)
    short_description = db.Column(db.Text)
    long_description = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    providers = db.relationship('Provider', back_populates='category', lazy='dynamic')