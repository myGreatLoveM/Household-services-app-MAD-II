from marshmallow import Schema, ValidationError, fields, validate, validates, pre_load
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


class CreateCategorySchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=3, max=20),
        error_messages={
            "required": "Category name is required.",
            "min": "Category name must be at least 3 characters long.",
            "max": "Category name must not exceed 20 characters."
        }
    )
    basePrice = fields.Number(
        required=True,
        validate=validate.Range(min=100),
        error_messages={
            "required": "Base price is required.",
            "min": "Base price must be at least 100 INR",
        }
    )
    minTime = fields.Number(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            "required": "Minimun time is required.",
            "min": "Minimun time must be at least 1 hr",
        }
    )
    serviceRate = fields.Number(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            "required": "Service rate is required.",
            "min": "Service rate must be at least 1%.",
        }
    )
    bookingRate = fields.Number(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            "required": "Booking rate is required.",
            "min": "Booking rate must be at least 1%.",
        }
    )
    transactionRate = fields.Number(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            "required": "Transaction rate is required.",
            "min": "Transaction rate must be at least 1%.",
        }
    )
    description = fields.String()