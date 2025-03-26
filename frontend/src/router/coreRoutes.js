import HomeView from '@/views/HomeView.vue'
import CategoriesExploreView from '@/views/core/CategoriesExploreView.vue'
import CategoryExploreView from '@/views/core/CategoryExploreView.vue'
import ActiveServicesExploreView from '@/views/core/ActiveServicesExploreView.vue'
import ActiveServiceView from '@/views/core/ActiveServiceView.vue'


export const coreRoutes = [
  {
    path: '',
    name: 'home',
    component: HomeView,
  },
  {
    path: 'categories',
    children: [
      {
        path: '',
        name: 'explore-categories',
        component: CategoriesExploreView,
      },
      {
        path: ':catId',
        name: 'explore-category',
        component: CategoryExploreView,
      },
    ],
  },
  {
    path: 'services',
    children: [
      {
        path: '',
        name: 'explore-listed-services',
        component: ActiveServicesExploreView,
      },
      {
        path: ':serviceId(\\d+)',
        name: 'explore-service',
        component: ActiveServiceView,
      },
    ],
  },
]
