import ProviderBookingsView from '@/views/provider/ProviderBookingsView.vue'
import ProviderDashboardView from '@/views/provider/ProviderDashboardView.vue'
import ProviderPendingBookingsView from '@/views/provider/ProviderPendingBookingsView.vue'
import ProviderProfileView from '@/views/provider/ProviderProfileView.vue'
import ProviderServicesView from '@/views/provider/ProviderServicesView.vue'

export const providerRoutes = [
  {
    path: '',
    name: 'provider-dashboard',
    component: ProviderDashboardView,
  },
  {
    path: 'services',
    name: 'provider-services',
    component: ProviderServicesView,
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
        path: 'pending',
        name: 'provider-pending-bookings',
        component: ProviderPendingBookingsView,
      },
    ],
  },
  {
    path: 'payments',
    name: 'provider-payments',
    component: ProviderDashboardView,
  },
  {
    path: 'profile',
    name: 'provider-profile',
    component: ProviderProfileView,
  },
]
