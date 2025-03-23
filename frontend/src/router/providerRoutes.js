import ProviderDashboardView from '@/views/provider/ProviderDashboardView.vue'

export const providerRoutes = [
  {
    path: '',
    name: 'provider-dashboard',
    component: ProviderDashboardView,
  },
  {
    path: 'services',
    name: 'provider-services',
    component: ProviderDashboardView,
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
    component: ProviderDashboardView,
  },
]
