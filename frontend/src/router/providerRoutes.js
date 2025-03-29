import ProviderBookingsView from '@/views/provider/ProviderBookingsView.vue'
import ProviderDashboardView from '@/views/provider/ProviderDashboardView.vue'
import ProviderPaymentsView from '@/views/provider/ProviderPaymentsView.vue'
import ProviderPendingBookingsView from '@/views/provider/ProviderPendingBookingsView.vue'
import ProviderProfileView from '@/views/provider/ProviderProfileView.vue'
import ProviderServicesView from '@/views/provider/ProviderServicesView.vue'
import ProviderSingleBookingView from '@/views/provider/ProviderSingleBookingView.vue'
import ProviderSingleServiceView from '@/views/provider/ProviderSingleServiceView.vue'

export const providerRoutes = [
  {
    path: '',
    name: 'provider-dashboard',
    component: ProviderDashboardView,
  },
  {
    path: 'services',
    children: [
      {
        path: '',
        name: 'provider-services',
        component: ProviderServicesView,
      },
      {
        path: ':serviceId(\\d+)',
        name: 'provider-single-service',
        component: ProviderSingleServiceView,
      },
    ],
  },
  {
    path: 'bookings',
    children: [
      {
        path: '',
        name: 'provider-bookings',
        component: ProviderBookingsView,
      },
      {
        path: ':bookingId(\\d+)',
        name: 'provider-single-booking',
        component: ProviderSingleBookingView,
      },
      {
        path: 'pending',
        name: 'provider-pending-bookings',
        component: ProviderPendingBookingsView,
      },
    ],
  },
  {
    path: 'payments',
    name: 'provider-payments',
    component: ProviderPaymentsView,
  },
  {
    path: 'profile',
    name: 'provider-profile',
    component: ProviderProfileView,
  },
]
