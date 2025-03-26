from flask_restful.reqparse import RequestParser
from application.enums import UserStatusEnum, ProviderServiceStatusEnum



admin_service_query_args_parser = RequestParser()
admin_service_query_args_parser.add_argument('page', type=int, location='args', default=1)
admin_service_query_args_parser.add_argument(
    'status', 
    location='args', 
    choices=[ProviderServiceStatusEnum.APPROVE.value, ProviderServiceStatusEnum.PENDING.value], 
    help='status should not be allowed to take other choices', 
    default=ProviderServiceStatusEnum.APPROVE.value
)



admin_provider_query_args_parser = RequestParser()
admin_provider_query_args_parser.add_argument('page', type=int, location='args', default=1)
admin_provider_query_args_parser.add_argument(
    'status', 
    location='args', 
    choices=[UserStatusEnum.APPROVE.value, UserStatusEnum.PENDING.value, UserStatusEnum.BLOCK.value], 
    help='status should not be allowed to take other choices', 
    default=UserStatusEnum.APPROVE.value
)