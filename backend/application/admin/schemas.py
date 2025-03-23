from application.extensions import ma
from .models import Category
from marshmallow import fields



class CategorySchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Category  
        load_instance = True
        include_fk = False
        include_relationships = False

    providers = fields.List(fields.Nested('ProviderSchema', many=True, exclude=['category']))
