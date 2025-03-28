import CustomerBookingsView from '@/views/customer/CustomerBookingsView.vue'
import CustomerDashboardView from '@/views/customer/CustomerDashboardView.vue'
import CustomerPaymentsView from '@/views/customer/CustomerPaymentsView.vue'
import CustomerPendingBookingsView from '@/views/customer/CustomerPendingBookingsView.vue'
import CustomerPendingPaymentsView from '@/views/customer/CustomerPendingPaymentsView.vue'
import CustomerProfileView from '@/views/customer/CustomerProfileView.vue'


export const customerRoutes = [
  {
    path: '',
    name: 'customer-dashboard',
    component: CustomerDashboardView,
  },
  {
    path: 'bookings',
    children: [
      {
        path: '',
        name: 'customer-bookings',
        component: CustomerBookingsView,
      },
      {
        path: 'pending',
        name: 'customer-pending-bookings',
        component: CustomerPendingBookingsView,
      },
    ],
  },
  {
    path: 'payments',
    children: [
      {
        path: '',
        name: 'customer-payments',
        component: CustomerPaymentsView,
      },
      {
        path: 'pending',
        name: 'customer-pending-payments',
        component: CustomerPendingPaymentsView,
      },
    ],
  },
  {
    path: 'profile',
    name: 'customer-profile',
    component: CustomerProfileView,
  },
]
