from flask import current_app
from flask_security import SQLAlchemyUserDatastore
import sqlalchemy as sa
import click

from application.extensions import db



@current_app.cli.command('create-role')
@click.argument('role')
@click.option("--desc", default='', type=str, help='Provide description for a role')
def create_role(role, desc):
    inspector = sa.inspect(db.engine)
    role_table = inspector.has_table('roles')

    if not role_table:
        raise Exception('Database has no Roles table.')

    if not role:
        raise Exception('Provide valid role name.')
    
    datastore : SQLAlchemyUserDatastore = current_app.security.datastore
    datastore.find_or_create_role(
        name=role, 
        description=desc
    )
    db.session.commit()
    print('Role created', role)
    return 