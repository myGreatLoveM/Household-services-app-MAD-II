from marshmallow import fields

from .models import Profile, Role, User

from application.extensions import ma
from application.customers.schemas import CustomerSchema
from application.providers.schemas import ProviderSchema
from application.enums import UserRoleEnum



class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        load_instance = True
        include_relationships = False
        fields = ('username', 'role', 'provider', 'customer', 'profile')

    role = fields.Method('get_role_from_relationship')
    provider = fields.Method('get_provider_relationship')
    customer = fields.Method('get_customer_relationship')
    profile = fields.Nested('ProfileSchema')

    # created_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    # updated_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    def get_role_from_relationship(self, obj):
        roles_schema = RoleSchema(many=True)
        roles = roles_schema.dump(obj.roles)
        return roles[0].get('name')

    def get_provider_relationship(self, obj):
        if any(role.name == UserRoleEnum.PROVIDER.value for role in obj.roles):
            return ProviderSchema(only=('id', 'is_approved', 'is_blocked')).dump(obj.provider)
        return None

    def get_customer_relationship(self, obj):
        if any(role.name == UserRoleEnum.CUSTOMER.value for role in obj.roles):
            return CustomerSchema(only=('id', 'is_blocked')).dump(obj.customer)
        return None



class RoleSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Role
        load_instance = True
        fields = ('name',)
        dump_only = ('name',)
        include_relationships = False


class ProfileSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Profile
        load_instance = True
        include_fk = False
        include_relationships = False
