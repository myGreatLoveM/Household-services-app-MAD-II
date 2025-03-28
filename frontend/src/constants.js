export const userRoles = ['customer', 'provider']

export const UserRoles = Object.freeze({
  ADMIN: 'admin',
  CUSTOMER: 'customer',
  PROVIDER: 'provider',
})


export const UserStatus = Object.freeze({
  APPROVED: 'approved',
  PENDING: 'pending',
  BLOCKED: 'blocked',
})


export const ServiceStatus = Object.freeze({
  APPROVED: 'approved',
  PENDING: 'pending',
  BLOCKED: 'blocked',
})


export const BookingStatus = Object.freeze({
  PENDING : 'pending',
  REJECT : 'rejected',
  CONFIRM : 'confirmed',
  CANCEL : 'cancelled',
  ACTIVE : 'active',
  COMPLETE : 'completed',
  CLOSE : 'closed',
})

export const PaymentStatus = Object.freeze({
  PENDING : 'pending',
  PAID : 'paid',
  CANCEL : 'cancelled'
})


export const PaymentMethods = Object.freeze({
  CREDIT_CARD: 'credit_card',
  PAYPAL: 'paypal',
  UPI: 'upi',
})
