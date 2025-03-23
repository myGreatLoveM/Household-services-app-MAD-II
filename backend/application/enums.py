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
    NOT_APPROVED = 'not-approved'
    BLOCK = 'block'
    UNBLOCK = 'unblock'


class ProviderServiceStatusEnum(Enum):
    APPROVE = 'approve'
    BLOCK = 'block'
    UNBLOCK = 'unblock'
    CONTINUE = 'continue'
    DISCONTINUE = 'discontinue'


class ProviderAvailabilityEnum(Enum):
    WEEKDAYS = 'weekdays'
    WEEKENDS = 'weekends'
    ALL_TIME = '24/7'


class BookingStatusEnum(Enum):
    PENDING = 'pending'
    CONFIRM = 'confirmed'
    REJECT = 'rejected'
    ACTIVE = 'active'
    COMPLETE = 'completed'
    CLOSE = 'closed'


class PaymentStatusEnum(Enum):
    PENDING = 'pending'
    PAID = 'paid'
    CANCELLED = 'cancelled'


class PaymentMethodEnum(Enum):
    CREDIT_CARD = 'credit_card'
    PAYPAL = 'paypal'
    UPI = 'upi'
