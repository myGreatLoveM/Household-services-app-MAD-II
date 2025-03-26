import { createRouter, createWebHistory } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '@/stores/authStore.js'
import { useAuthUserStore } from '@/stores/authUserStore.js'

import AppLayout from '@/layouts/AppLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import CustomerLayout from '@/layouts/CustomerLayout.vue'
import ProviderLayout from '@/layouts/ProviderLayout.vue'

import { coreRoutes } from '@/router/coreRoutes.js'
import { authRoutes } from '@/router/authRoutes.js'
import { adminRoutes } from '@/router/adminRoutes.js'
import { customerRoutes } from '@/router/customerRoutes.js'
import { providerRoutes } from '@/router/providerRoutes.js'

import ProviderNotApprovedView from '@/views/error/ProviderNotApprovedView.vue'
import UserBlockedView from '@/views/error/UserBlockedView.vue'
import NotFoundView from '@/views/error/NotFoundView.vue'
import ServerErrorView from '@/views/error/ServerErrorView.vue'
import UnauthorizedView from '@/views/error/UnauthorizedView.vue'

import { UserRoles } from '@/constants.js'

const toast = useToast()

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '',
      component: AppLayout,
      children: coreRoutes,
    },
    {
      path: '/auth',
      name: 'auth',
      component: AppLayout,
      beforeEnter: (to, from, next) => {
        const authStore = useAuthStore()

        if (authStore.isAuthenticated && to.name !== 'logout') {
          next(from)
        } else {
          next()
        }
      },
      redirect: { name: 'login' },
      children: authRoutes,
    },
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true, roles: [UserRoles.ADMIN] },
      children: adminRoutes,
    },
    {
      path: '/customers/:custId(\\d+)',
      component: CustomerLayout,
      meta: { requiresAuth: true, roles: [UserRoles.CUSTOMER] },
      beforeEnter: (to, from, next) => {
        const authUserStore = useAuthUserStore()
        const currentCustId = authUserStore.customer.id
        const targetCustId = to.params.custId

        if (currentCustId !== parseInt(targetCustId)) {
          next({ name: 'unauthorized' })
        } else if (authUserStore.isCustomerBlocked) {
          next({ name: 'customer-blocked', params: { custId: currentCustId } })
        } else {
          next()
        }
      },
      children: customerRoutes,
    },
    {
      path: '/providers/:provId(\\d+)',
      component: ProviderLayout,
      meta: { requiresAuth: true, roles: [UserRoles.PROVIDER] },
      beforeEnter: (to, from, next) => {
        const authUserStore = useAuthUserStore()
        const currentProvId = authUserStore.provider.id
        const targetProvId = parseInt(to.params.provId)

        if (currentProvId !== targetProvId) {
          next({ name: 'unauthorized' })
        } else if (!authUserStore.isProviderApproved) {
          console.log('provider not approved')
          next({ name: 'provider-not-approved', params: { provId: currentProvId } })
        } else if (authUserStore.isProviderBlocked) {
          next({ name: 'provider-blocked', params: { provId: currentProvId } })
        } else {
          next()
        }
      },
      children: providerRoutes,
    },
    {
      path: '/providers/:provId(\\d+)/not-approved',
      name: 'provider-not-approved',
      component: ProviderNotApprovedView,
      meta: { requiresAuth: true, roles: [UserRoles.PROVIDER] },
    },
    {
      path: '/providers/:provId(\\d+)/blocked',
      name: 'provider-blocked',
      component: UserBlockedView,
      meta: { requiresAuth: true, roles: [UserRoles.PROVIDER] },
    },
    {
      path: '/customers/:custId(\\d+)/blocked',
      name: 'customer-blocked',
      component: UserBlockedView,
      meta: { requiresAuth: true, roles: [UserRoles.CUSTOMER] },
    },
    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: UnauthorizedView,
    },
    {
      path: '/500',
      name: 'server-error',
      component: ServerErrorView,
    },
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: NotFoundView, // Handles undefined paths
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const authUserStore = useAuthUserStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    toast.error('User is not loggedin!!')
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresAuth && to.meta.roles && !to.meta.roles.includes(authUserStore.role)) {
    next({ name: 'unauthorized' })
  } else {
    next()
  }
})

export default router
