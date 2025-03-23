import HomeView from '@/views/HomeView.vue'
import CategoriesExploreView from '@/views/core/CategoriesExploreView.vue'
import CategoryExploreView from '@/views/core/CategoryExploreView.vue'
import ServiceExploreView from '@/views/core/ServiceExploreView.vue'


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
    name: 'explore-listed-services',
    component: ServiceExploreView,
  },
]
