import CustomerDashboardView from '@/views/customer/CustomerDashboardView.vue'


export const customerRoutes = [
  {
    path: '',
    name: 'customer-dashboard',
    component: CustomerDashboardView,
    params: true,
    props: true,
  },
  {
    path: 'bookings',
    name: 'customer-bookings',
    component: CustomerDashboardView,
    params: true,
    props: true,
  },
  {
    path: 'payments',
    name: 'customer-payments',
    component: CustomerDashboardView,
    params: true,
    props: true,
  },
  {
    path: 'profile',
    name: 'customer-profile',
    component: CustomerDashboardView,
    params: true,
    props: true,
  },
]
