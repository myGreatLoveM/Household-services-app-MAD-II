<script setup>
import { reactive, watch, ref, computed } from 'vue'
import { useAuthStore } from '@/stores/authStore.js'
import { useToast } from 'vue-toastification'
import { validateLoginForm } from '@/validations/authFormValidation.js'
import InputField from '@/components/InputField.vue'


const { login } = useAuthStore()
const toast = useToast()

const formFields = {
  username: '',
  password: '',
}

const loginForm = reactive({ ...formFields })
const loginFormErrors = reactive({ ...formFields })
const isLoading = ref(false)

watch(
  () => ({ ...loginForm }),
  () => {
    validateLoginForm(loginForm, loginFormErrors)
  },
  { deep: true },
)

const isloginFormButtonDisabled = computed(() => {
  return loginForm.password === '' || Object.values(loginFormErrors).some((err) => err !== '')
})

const handleLogin = async () => {
  const isLoginFormValid = validateLoginForm(loginForm, loginFormErrors)

  if (isLoginFormValid || !isloginFormButtonDisabled.value) {
    isLoading.value = true
    try {
      await login({...loginForm})
      toast.success('User logged in successfully')
    } catch (error) {
      toast.error(error.message || 'An error occurred during login.')
    } finally {
      isLoading.value = false
    }
  } else {
    toast.error('Something went wrong while logging.')
  }
}
</script>

<template>
  <div class="w-full h-full flex items-center justify-center px-2 py-6 sm:px-6 sm:py-16 lg:px-8">
    <div class="w-full px-2 sm:w-[500px] sm:px-6 sm:py-4">
      <h2 class="text-center text-2xl font-bold leading-tight text-black mb-4">
        Log in to your account
      </h2>

      <form class="space-y-6" @submit.prevent="handleLogin">
        <InputField
          id="username"
          label="Username"
          type="text"
          placeholder="Enter your username"
          v-model="loginForm.username"
          :error="loginFormErrors.username"
        />
        <InputField
          id="password"
          label="Password"
          type="password"
          placeholder="Enter your password"
          v-model="loginForm.password"
          :error="loginFormErrors.password"
        />
        <button
          type="submit"
          :disabled="isloginFormButtonDisabled || isLoading"
          :class="isloginFormButtonDisabled || isLoading ? 'bg-black/50 hover:bg-black/50 cursor-none' : 'bg-black hover:bg-black/80'"
          class="inline-flex w-full items-center justify-center rounded-md bg-black px-3.5 py-2.5 font-semibold leading-7 text-white hover:bg-black/80 disabled:bg-gray-600"
        >
          {{ !isLoading ? 'Login' : 'Logging....' }}
        </button>
      </form>

      <p class="mt-4 text-center text-sm text-gray-600">Don't have an account?</p>

      <div class="flex flex-col items-center gap-1 mt-2">
        <RouterLink
          :to="{ name: 'register', params: { role: 'customer' } }"
          class="font-semibold text-sm text-black transition-all duration-200 hover:underline"
        >
          Register as customer
        </RouterLink>
        <RouterLink
          :to="{ name: 'register', params: { role: 'provider' } }"
          class="font-semibold text-sm text-black transition-all duration-200 hover:underline"
        >
          Register as service provider
        </RouterLink>
      </div>
    </div>
  </div>
</template>
