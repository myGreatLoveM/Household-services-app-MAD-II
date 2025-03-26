import { defineStore } from 'pinia'
import { useAuthUserStore } from '@/stores/authUserStore.js'
import { loginUserService, refreshTokens, registerUserService } from '@/services/authService.js'
import { useToast } from 'vue-toastification'

const toast = useToast()

export const useAuthStore = defineStore('authStore', {
  state: () => {
    return {
      authToken: JSON.parse(localStorage.getItem('auth-token')) || null,
      isAuthenticated: !!localStorage.getItem('auth-token') && !!localStorage.getItem('user'),
    }
  },
  actions: {
    async login(formData) {
      try {
        const data = await loginUserService(formData)
        const authUserStore = useAuthUserStore()

        authUserStore.setUser(data?.user)

        localStorage.setItem('auth-token', JSON.stringify(data?.access_token))
        localStorage.setItem('refresh-token', JSON.stringify(data?.refresh_token))

        this.authToken = data?.access_token
        this.isAuthenticated = !!this.authToken && !!authUserStore.username && !!authUserStore.role

        if (!this.isAuthenticated) {
          throw new Error('User not authenticated properly!!')
        }

        const redirectUrl = this.router.currentRoute.value.query.redirect
        if (redirectUrl) {
          return this.router.push({ path: redirectUrl })
        }

        authUserStore.redirectUserDashboard()
        return
      } catch (error) {
        throw new Error(error.message || 'Something went wrong while logging!!')
      }
    },
    async register(formData, role) {
      try {
        await registerUserService(formData, role)
        this.router.push({ name: 'login' })
      } catch (error) {
        throw new Error(error.message || 'Something went wrong during registration')
      }
    },
    logout() {
      const authUserStore = useAuthUserStore()
      authUserStore.clearUser()

      this.authToken = null
      this.isAuthenticated = false

      localStorage.removeItem('auth-token')
      localStorage.removeItem('refresh-token')

      toast.success('User logged out successfully')
      return this.router.push({ name: 'home' })
    },
    async refreshExpiredAuthToken() {
      try {
        const data = await refreshTokens()

        localStorage.setItem('auth-token', JSON.stringify(data?.access_token))
        localStorage.setItem('refresh-token', JSON.stringify(data?.refresh_token))

        this.authToken = data?.access_token
        console.log('tokens refreshed')
      } catch (error) {
        console.log(error)
      }
    },
  },
})
