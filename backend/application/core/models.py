from flask_security import UserMixin, RoleMixin
from application.extensions import db
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    fs_uniquifier = db.Column(db.String(300), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    roles = db.relationship('Role', back_populates='bearers', secondary='user_roles', cascade='all,delete')
    admin = db.relationship('Admin', uselist=False)
    provider = db.relationship('Provider', back_populates='user', uselist=False)
    customer = db.relationship('Customer', back_populates='user', uselist=False)
    profile = db.relationship('Profile', uselist=False, cascade='all, delete')

    __table_args__ = (
        db.UniqueConstraint('username', 'email', name='uq__users__username__email'),
    )


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    bearers = db.relationship('User', back_populates='roles', secondary='user_roles')


class UserRole(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk__user_roles__users__user_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', name='fk__user_roles__roles__role_id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'role_id', name='uq__user_roles__user_id__role_id'),
    )


class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk__profiles__users__user_id'), nullable=False)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    sex = db.Column(db.String(10))
    age = db.Column(db.Integer)
    contact = db.Column(db.String(20))
    bio = db.Column(db.Text)
    location = db.Column(db.String(30))
    

    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        db.UniqueConstraint('user_id', name='uq__profiles__user_id'),
    )


