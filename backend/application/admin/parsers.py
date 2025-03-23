from flask_restful.reqparse import RequestParser
from application.enums import UserStatusEnum



admin_provider_query_args_parser = RequestParser()
admin_provider_query_args_parser.add_argument('page', type=int, location='args', nullable=True)
admin_provider_query_args_parser.add_argument('status', location='args', choices=[UserStatusEnum.APPROVE.value, UserStatusEnum.NOT_APPROVED.value, UserStatusEnum.BLOCK.value], help='status should not be allowed to take other choices', nullable=True)