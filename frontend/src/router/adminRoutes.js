import AdminBookingView from '@/views/admin/AdminBookingView.vue'
import AdminCategoryView from '@/views/admin/AdminCategoryView.vue'
import AdminCustomerView from '@/views/admin/AdminCustomerView.vue'
import AdminPaymentView from '@/views/admin/AdminPaymentView.vue'
import AdminProviderView from '@/views/admin/AdminProviderView.vue'
import AdminServiceView from '@/views/admin/AdminServiceView.vue'
import AdminDashboardView from '@/views/admin/AdminDashboardView.vue'
import AdminNewProvidersView from '@/views/admin/AdminNewProvidersView.vue'

export const adminRoutes = [
  {
    path: '',
    name: 'admin-dashboard',
    component: AdminDashboardView,
  },
  {
    path: 'categories',
    name: 'admin-categories',
    component: AdminCategoryView,
  },
  {
    path: 'services',
    name: 'admin-services',
    component: AdminServiceView,
  },
  {
    path: 'providers',
    name: 'admin-providers',
    component: AdminProviderView,
  },
  {
    path: 'providers/not-approved',
    name: 'admin-providers-not-approved',
    component: AdminNewProvidersView
  },
  {
    path: 'customers',
    name: 'admin-customers',
    component: AdminCustomerView,
  },
  {
    path: 'bookings',
    name: 'admin-bookings',
    component: AdminBookingView,
  },
  {
    path: 'payments',
    name: 'admin-payments',
    component: AdminPaymentView,
  },
]
