import AdminBookingsView from '@/views/admin/AdminBookingsView.vue'
import AdminCategoriesView from '@/views/admin/AdminCategoriesView.vue'
import AdminCustomersView from '@/views/admin/AdminCustomersView.vue'
import AdminPaymentsView from '@/views/admin/AdminPaymentsView.vue'
import AdminProvidersView from '@/views/admin/AdminProvidersView.vue'
import AdminServicesView from '@/views/admin/AdminServicesView.vue'
import AdminDashboardView from '@/views/admin/AdminDashboardView.vue'
import AdminPendingProvidersView from '@/views/admin/AdminPendingProvidersView.vue'
import AdminSingleCategoryView from '@/views/admin/AdminSingleCategoryView.vue'
import AdminSingleServiceView from '@/views/admin/AdminSingleServiceView.vue'
import AdminPendingServicesView from '@/views/admin/AdminPendingServicesView.vue'




export const adminRoutes = [
  {
    path: '',
    name: 'admin-dashboard',
    component: AdminDashboardView,
  },
  {
    path: 'categories',
    children: [
      {
        path: '',
        name: 'admin-categories',
        component: AdminCategoriesView,
      },
      {
        path: ':catId(\\d+)',
        name: 'admin-single-category',
        component: AdminSingleCategoryView,
      },
    ],
  },
  {
    path: 'services',
    children: [
      {
        path: '',
        name: 'admin-services',
        component: AdminServicesView,
      },
      {
        path: ':serviceId(\\d+)',
        name: 'admin-single-service',
        component: AdminSingleServiceView,
      },
      {
        path: 'pending',
        name: 'admin-services-pending',
        component: AdminPendingServicesView,
      },
    ],
  },
  {
    path: 'providers',
    children: [
      {
        path: '',
        name: 'admin-providers',
        component: AdminProvidersView,
      },
      {
        path: 'pending',
        name: 'admin-providers-pending',
        component: AdminPendingProvidersView,
      },
    ],
  },
  {
    path: 'customers',
    name: 'admin-customers',
    component: AdminCustomersView,
  },
  {
    path: 'bookings',
    name: 'admin-bookings',
    component: AdminBookingsView,
  },
  {
    path: 'payments',
    name: 'admin-payments',
    component: AdminPaymentsView,
  },
]
