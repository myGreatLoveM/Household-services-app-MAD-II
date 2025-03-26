import ProviderDashboardView from '@/views/provider/ProviderDashboardView.vue'
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
    name: 'provider-bookings',
    component: ProviderDashboardView,
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
