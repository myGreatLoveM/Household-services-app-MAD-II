<script setup>
import { reactive, watch, computed, onBeforeMount, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore.js'
import { useToast } from 'vue-toastification'

import InputField from '@/components/InputField.vue'
import SelectField from '@/components/SelectField.vue'

import { validateRegisterForm } from '@/validations/authFormValidation.js'
import { getAllCategoriesForRegisterForm } from '@/services/authService.js'

import { UserRoles } from '@/constants.js'
import { trimObjectStringValues } from '@/utils.js'


const { register } = useAuthStore()
const toast = useToast()
const route = useRoute()

const role = route.params.role

const providerSpecificField = {
  category: '',
  experience: '',
}

let registerFormField = {
  username: '',
  email: '',
  gender: '',
  contact: '',
  location: '',
  password: '',
  confirmPassword: '',
}

if (role === UserRoles.PROVIDER) {
  registerFormField = { ...registerFormField, ...providerSpecificField }
}

const registerForm = reactive({ ...registerFormField })
const registerFormErrors = reactive({ ...registerFormField })
const categoryChoices = ref([])
const isLoading = ref(false)

const genderChoices = [
  { label: 'Male', value: 'male' },
  { label: 'Female', value: 'female' },
]

onBeforeMount(async () => {
  try {
    const categories = await getAllCategoriesForRegisterForm()
    const formFieldChoices = categories.map((cat) => ({ label: cat, value: cat }))

    categoryChoices.value.push(...formFieldChoices)
  } catch (error) {
    toast.error(error.message)
  }
})

watch(
  () => ({ ...registerForm }),
  () => {
    validateRegisterForm(registerForm, registerFormErrors, role)
  },
  { deep: true },
)

const isRegisterFormButtonDisabled = computed(() => {
  return registerForm.password === '' || registerForm.password !== registerForm.confirmPassword || Object.values(registerFormErrors).some((err) => err !== '')
})

const handleRegister = async () => {
  const isRegisterFormValid = validateRegisterForm(registerForm, registerFormErrors, role)

  if (isRegisterFormValid || !isRegisterFormButtonDisabled.value) {
    isLoading.value = true
    try {
      let { confirmPassword, ...formData } = registerForm
      let experience = null

      if (role === UserRoles.PROVIDER) {
        experience = parseInt(formData.experience)
        formData = { ...formData, experience }
      }

      await register(trimObjectStringValues(formData), role)
      toast.success('User registered successfully')
    } catch (error) {
      toast.error(error.message || 'An error occurred during registration.')
    } finally {
      isLoading.value = false
    }
  } else {
      toast.error('Something went wrong while registering.')
  }
}
</script>

<template>
  <div
    class="w-full h-full flex items-center justify-center px-4 py-10 sm:px-6 sm:py-16 lg:px-8 lg:py-8"
  >
    <div class="w-full px-2 sm:w-[500px] sm:px-6 sm:py-4">
      <h2 class="text-center text-2xl font-bold leading-tight text-black mb-4">
        Register with us as <span id="role-type">{{ role }}</span>
      </h2>

      <form class="space-y-5" @submit.prevent="handleRegister">
        <InputField
          id="username"
          label="Username"
          type="text"
          placeholder="Enter your username"
          v-model="registerForm.username"
          :error="registerFormErrors.username"
        />

        <InputField
          id="email"
          label="Email"
          type="email"
          placeholder="Enter your email"
          v-model="registerForm.email"
          :error="registerFormErrors.email"
        />

        <SelectField
          id="gender"
          label="Gender"
          placeholder="Select your gender"
          v-model="registerForm.gender"
          :choices="genderChoices"
          :error="registerFormErrors.gender"
        />

        <SelectField
          id="category"
          label="Category"
          placeholder="Select your category"
          v-model="registerForm.category"
          :choices="categoryChoices"
          :error="registerFormErrors.category"
          v-if="role === 'provider'"
        />

        <InputField
          id="experience"
          label="Experience"
          type="number"
          placeholder="Enter your experience"
          v-model="registerForm.experience"
          :error="registerFormErrors.experience"
          v-if="role === 'provider'"
        />

        <InputField
          id="loaction"
          label="Location"
          type="text"
          placeholder="Enter your location"
          v-model="registerForm.location"
          :error="registerFormErrors.location"
        />

        <InputField
          id="contact"
          label="Contact"
          type="text"
          placeholder="Enter your contact number"
          v-model="registerForm.contact"
          :error="registerFormErrors.contact"
        />

        <InputField
          id="password"
          label="Password"
          type="password"
          placeholder="Enter your password"
          v-model="registerForm.password"
          :error="registerFormErrors.password"
        />

        <InputField
          id="confirm_password"
          label="Confirm Password"
          type="text"
          placeholder="Enter your password again"
          v-model="registerForm.confirmPassword"
          :error="registerFormErrors.confirmPassword"
        />

        <button
          type="submit"
          :disabled="isRegisterFormButtonDisabled || isLoading"
          :class="isRegisterFormButtonDisabled || isLoading ? 'bg-black/50 hover:bg-black/50 cursor-none' : 'bg-black hover:bg-black/80'"
          class="inline-flex w-full items-center justify-center rounded-md px-3.5 py-2.5 font-semibold leading-7 text-white "
        >
          {{ !isLoading ? 'Register' : 'Registering.....' }}
        </button>
      </form>

      <p class="mt-4 text-center text-sm text-gray-600">
        Already have an account?
        <RouterLink
          :to="{ name: 'login' }"
          class="font-semibold text-sm text-black transition-all duration-200 hover:underline"
        >
          Login
        </RouterLink>
      </p>
    </div>
  </div>
</template>
