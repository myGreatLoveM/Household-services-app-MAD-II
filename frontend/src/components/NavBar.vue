<script setup>
import { RouterLink } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthUserStore } from '@/stores/authUserStore.js'
import { UserRoles } from '@/constants.js'
import { ref } from 'vue'

defineProps({
  isModalOpen: {
    type: Boolean,
  },
})

const authUserStore = useAuthUserStore()

const { username, role, provider, customer } = storeToRefs(authUserStore)

const dashboard = ref(null)

if (role.value === UserRoles.ADMIN) {
  dashboard.value = { name: 'admin-dashboard' }
} else if (role.value === UserRoles.PROVIDER) {
  dashboard.value = { name: 'provider-dashboard', params: { provId: provider.value.id } }
} else if (role.value === UserRoles.CUSTOMER) {
  dashboard.value = { name: 'customer-dashboard', params: { custId: customer.value.id } }
}
</script>

<template>
  <header :class="isModalOpen && 'opacity-50'">
    <nav class="relative w-full">
      <div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-4">
        <div class="inline-flex items-center space-x-2">
          <RouterLink :to="{ name: 'home' }" class="font-bold text-xl tracking-wide">
            HouseHelpNow
          </RouterLink>
        </div>

        <div class="space-x-5 lg:block">
          <RouterLink
            to="/categories"
            class="text-md font-semibold text-gray-400 hover:text-gray-700"
          >
            categories
          </RouterLink>
          <RouterLink
            to="/services"
            class="text-md font-semibold text-gray-400 hover:text-gray-700"
          >
            services
          </RouterLink>

          <span v-if="username" class="space-x-3">
            <RouterLink
              v-if="dashboard"
              :to="dashboard"
              class="text-green-500 hover:bg-green-50 text-xl font-bold py-0.5 px-5 rounded-full border-2 border-green-200"
            >
              {{ username }}
            </RouterLink>
          </span>

          <RouterLink
            v-else
            :to="{ name: 'login' }"
            class="rounded-md border border-black px-4 py-2 text-sm font-semibold text-black shadow-sm hover:bg-gray-100"
          >
            Login
          </RouterLink>
        </div>
      </div>
    </nav>
  </header>
</template>
