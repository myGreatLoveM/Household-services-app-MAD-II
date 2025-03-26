import { UserRoles } from '@/constants'
import { defineStore } from 'pinia'


export const useAuthUserStore = defineStore('authUserStore', {
  state: () => ({
    username: (() => {
      try {
        return JSON.parse(localStorage.getItem('user'))?.username || null
      } catch (e) {
        console.log(e.message)
        return null
      }
    })(),
    role: (() => {
      try {
        return JSON.parse(localStorage.getItem('user'))?.role || null
      } catch (e) {
        console.log(e.message)
        return null
      }
    })(),
    provider: (() => {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (user?.role !== UserRoles.PROVIDER) {
          return {
            id: null,
            isApproved: null,
            isBlocked: null,
          }
        }
        const provider = user?.provider
        return {
          id: provider?.id || null,
          isApproved: provider?.is_approved ?? null,
          isBlocked: provider?.is_blocked ?? null,
        }
      } catch (e) {
        console.log(e.message)
        return {
          id: null,
          isApproved: null,
          isBlocked: null,
        }
      }
    })(),
    customer: (() => {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (user?.role !== UserRoles.CUSTOMER) {
          return {
            id: null,
            isBlocked: null,
          }
        }
        const customer = user?.customer
        return {
          id: customer?.id || null,
          isBlocked: customer?.is_blocked ?? null,
        }
      } catch (e) {
        console.log(e.message)
        return {
          id: null,
          isBlocked: null,
        }
      }
    })(),
  }),
  actions: {
    setUser(user) {
      localStorage.setItem('user', JSON.stringify(user))

      this.username = user?.username || null
      this.role = user?.role || null

      if (this.role === UserRoles.PROVIDER) {
        this.provider = {
          id: user?.provider?.id || null,
          isApproved: user?.provider?.is_approved ?? null,
          isBlocked: user?.provider?.is_blocked ?? null,
        }
      } else if (this.role === UserRoles.CUSTOMER) {
        this.customer = {
          id: user?.customer?.id || null,
          isBlocked: user?.customer?.is_blocked ?? null,
        }
      }
    },
    clearUser() {
      this.username = null
      this.role = null
      this.provider = {}
      this.customer = {}

      localStorage.removeItem('user')
    },
    redirectUserDashboard() {
      if (this.role === UserRoles.ADMIN) {
        return this.router.push({ name: 'admin-dashboard' })
      } else if (this.role === UserRoles.PROVIDER) {
        console.log('redirect provider dashboard')
        return this.router.push({
          name: 'provider-dashboard',
          params: { provId: this.provider?.id },
        })
      } else if (this.role === UserRoles.CUSTOMER) {
        console.log('redirect to customer route')
        return this.router.push({
          name: 'customer-dashboard',
          params: { custId: this.customer?.id },
        })
      }

      return this.router.push({ name: 'home' })
    },
  },
  getters: {
    isAdmin: (state) => state.role === UserRoles.ADMIN,
    isProvider: (state) => state.role === UserRoles.PROVIDER,
    isCustomer: (state) => state.role === UserRoles.CUSTOMER,
    isProviderApproved: (state) => state.provider?.isApproved ?? null,
    isProviderBlocked: (state) => state.provider?.isBlocked ?? null,
    isCustomerBlocked: (state) => state.customer?.isBlocked ?? null
  },
})
