from enum import Enum

class UserRoleEnum(Enum):
    ADMIN = 'admin'
    PROVIDER = 'provider'
    CUSTOMER = 'customer'


class UserGenderEnum(Enum):
    MALE = 'male'
    FEMALE = 'female'


class UserStatusEnum(Enum):
    APPROVE = 'approved'
    PENDING = 'pending'
    BLOCK = 'blocked'
    UNBLOCK = 'unblocked'


class ProviderServiceStatusEnum(Enum):
    APPROVE = 'approved'
    PENDING = 'pending'
    BLOCK = 'blocked'
    UNBLOCK = 'unblocked'
    CONTINUE = 'continue'
    DISCONTINUE = 'discontinue'


class ProviderAvailabilityEnum(Enum):
    WEEKDAYS = 'weekdays'
    WEEKENDS = 'weekends'
    ALL_TIME = '24/7'


class BookingStatusEnum(Enum):
    PENDING = 'pending'
    REJECT = 'rejected'
    CONFIRM = 'confirmed'
    CANCEL = 'cancelled'
    ACTIVE = 'active'
    COMPLETE = 'completed'
    CLOSE = 'closed'


class PaymentStatusEnum(Enum):
    PENDING = 'pending'
    PAID = 'paid'
    CANCEL = 'cancelled'


class PaymentMethodEnum(Enum):
    CREDIT_CARD = 'credit_card'
    PAYPAL = 'paypal'
    UPI = 'upi'
