from marshmallow import Schema, ValidationError, fields, validate, validates
import regex as re

from application.enums import UserGenderEnum
from application.admin.seed_data import categories


class UserLoginSchema(Schema):
    username = fields.String(
        required=True,
        validate=validate.Length(min=3, max=20),
        error_messages={
            "required": "Username is required.",
            "min": "Username must be at least 3 characters long.",
            "max": "Username must not exceed 20 characters."
        }
    )
    password = fields.String(
        required=True,
        validate=validate.Length(min=6, max=20),
        error_messages={
            "required": "Password is required.",
            "min": "Password must be at least 6 characters long.",
            "max": "Password must not exceed 20 characters."
        }
    )

    @validates('username')
    def validate_username(self, value):
        if not re.match("^[a-zA-Z0-9]+$", value):
            raise ValidationError("Username must not contain special characters. Only letters and numbers are allowed.")



class UserRegisterSchema(Schema):
    username = fields.String(
        required=True,
        validate=validate.Length(min=3, max=20),
        error_messages={
            "required": "Username is required.",
            "min": "Username must be at least 3 characters long.",
            "max": "Username must not exceed 20 characters."
        }
    )
    email = fields.Email(
        required=True, 
        error_messages={"required": "Email is required."}
    )
    contact = fields.String(
        required=True, 
        validate=validate.Length(equal=10, error="Contact should be exact 10 number."), 
        error_messages={"required": "Age is required."}
    )
    gender = fields.String(
        required=True,
        validate=validate.OneOf([gender.value for gender in UserGenderEnum]),
        error_messages={"required": "Gender is required."}
    )
    location = fields.String(
        required=True,
        validate=validate.Length(min=5, max=20),
        error_messages={
            "required": "Location is required.",
            "min": "Location must be at least 5 characters long.",
            "max": "Location must not exceed 20 characters."
        }
    )
    password = fields.String(
        required=True,
        validate=validate.Length(min=6, max=20),
        error_messages={
            "required": "Password is required.",
            "min": "Password must be at least 6 characters long.",
            "max": "Password must not exceed 20 characters."
        }
    )


class ProviderRegisterSchema(UserRegisterSchema):
    experience = fields.Integer(
        required=True,
        validate=validate.Range(min=1, error="Experience should be atleast 1 year."), 
        error_messages={"required": "Experience is required."}
    )
    category = fields.String(
        required=True,
        validate=validate.OneOf([category['name'] for category in categories]),
        error_messages={"required": "Category is required."}
    )


