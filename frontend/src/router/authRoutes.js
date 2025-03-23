import { useAuthStore } from '@/stores/authStore.js'

import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import { UserRoles } from '@/constants.js'


export const authRoutes = [
  {
    path: 'login',
    name: 'login',
    component: LoginView,
  },
  {
    path: 'register/:role',
    name: 'register',
    component: RegisterView,
    beforeEnter: (to, from, next) => {
      const roleToCheck = to.params.role

      if (roleToCheck !== UserRoles.ADMIN && Object.values(UserRoles).includes(roleToCheck)) {
        next()
      } else {
        next({ name: 'not-found', params: { catchAll: to.fullPath } })
      }
    },
  },
  {
    path: 'logout',
    name: 'logout',
    beforeEnter: (to, from, next) => {
      const authStore = useAuthStore()
      authStore.logout()
      next({ name: 'home' })
    },
  },
]
