import sqlalchemy as sa
from flask import current_app
from flask_security import hash_password, SQLAlchemyUserDatastore
from sqlalchemy.exc import SQLAlchemyError
from .extensions import db
from configs import Config
from application.admin.models import Category, Admin
from application.admin.seed_data import categories as categories_raw_data


def create_initial_data(config: Config):
    inspector = sa.inspect(db.engine)

    user_table = inspector.has_table('users')
    role_table = inspector.has_table('roles')
    admin_table = inspector.has_table('admins')
    categories_table = inspector.has_table('categories')
    database_created = user_table and role_table and admin_table and categories_table

    if database_created:
        datastore : SQLAlchemyUserDatastore = current_app.security.datastore

        datastore.find_or_create_role(name='admin', description='This is superuser.')
        datastore.find_or_create_role(name='provider', description='This is service professional')
        datastore.find_or_create_role(name='customer', description='This is normal user.')
        db.session.commit()

        admin_user = datastore.find_user(email=config.ADMIN_EMAIL)

        if not admin_user:
            admin_user = datastore.create_user(
                username='admin', 
                email='admin@househelpnow.com', 
                password_hash=hash_password(config.ADMIN_PASSWORD), 
                roles=['admin'],
            )
            admin_user.admin = Admin()
            # new_admin = Admin()
            # new_admin.user_id = admin_user.id
            # db.session.add(new_admin)
            db.session.commit()

        admin = admin_user.admin

        if admin and admin.categories.count() != len(categories_raw_data):
            try:
                for cat in categories_raw_data:
                    cat_exists = Category.query.filter(Category.name == cat.get('name')).first()

                    if cat_exists:
                        continue

                    new_cat = Category(
                        name=cat.get('name'), 
                        admin_id=admin.id,
                        base_price=int(cat.get('base_price')),
                        commission_rate=int(cat.get('commission_rate')),
                        booking_rate=int(cat.get('booking_rate')),
                        transaction_rate=int(cat.get('transaction_rate')),
                        short_description=cat.get('short_description'),
                        long_description=cat.get('long_description'),
                    )
                    db.session.add(new_cat)
                db.session.commit()
                print('Everything created successfully')
            except:
                db.session.rollback()
                raise SQLAlchemyError('Something went wrong')
        db.session.commit()
    else:
        db.create_all()
    return