from application.extensions import ma
from .models import Customer



class CustomerSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Customer
        load_instance = True
        include_relationships = False