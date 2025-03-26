<script setup>
import { storeToRefs } from 'pinia'
import { useAuthUserStore } from '@/stores/authUserStore.js'
import { UserRoles } from '@/constants.js'

defineProps({
  dashboardPath: {
    type: String,
    required: true,
  },
  otherPaths: {
    type: Array,
  },
  isModalOpen: {
    type: Boolean,
  },
})

const authUserStore = useAuthUserStore()
const { role, provider, customer } = storeToRefs(authUserStore)
</script>

<template>
  <aside
    :class="isModalOpen && 'opacity-50'"
    class="flex max-h-screen w-64 flex-col overflow-y-auto border-r bg-white px-5 py-8"
  >
    <RouterLink :to="{ name: 'home' }" class="font-bold text-xl tracking-wide">
      HouseHelpNow
    </RouterLink>

    <div class="mt-6 flex flex-1 flex-col justify-between">
      <nav class="-mx-3 space-y-5">
        <div class="space-y-3">
          <RouterLink
            :to="{ name: dashboardPath }"
            class="flex items-center rounded-lg px-3 py-2 text-gray-600 transition-colors duration-300 hover:bg-gray-100 hover:text-gray-700"
            exact-active-class="bg-gray-100 text-gray-700"
          >
            <span class="mx-2 text-xl font-semibold">Dashboard</span>
          </RouterLink>
        </div>

        <div class="space-y-2" v-for="(path, i) in otherPaths" :key="i">
          <RouterLink
            v-if="role === UserRoles.PROVIDER"
            :to="{ name: path?.pathName, params: { provId: provider.id } }"
            class="flex items-center rounded-lg px-3 py-2 text-gray-600 transition-colors duration-300 hover:bg-gray-100 hover:text-gray-700"
            exact-active-class="bg-gray-100 text-gray-700"
          >
            <span class="mx-2 text-xl font-semibold">{{ path?.name }}</span>
          </RouterLink>
          <RouterLink
            v-else-if="role === UserRoles.CUSTOMER"
            :to="{ name: path?.pathName, params: { custId: customer.id } }"
            class="flex items-center rounded-lg px-3 py-2 text-gray-600 transition-colors duration-300 hover:bg-gray-100 hover:text-gray-700"
            exact-active-class="bg-gray-100 text-gray-700"
          >
            <span class="mx-2 text-xl font-semibold">{{ path?.name }}</span>
          </RouterLink>
          <RouterLink
            v-else-if="role === UserRoles.ADMIN"
            :to="{ name: path?.pathName }"
            class="flex items-center rounded-lg px-3 py-2 text-gray-600 transition-colors duration-300 hover:bg-gray-100 hover:text-gray-700"
            exact-active-class="bg-gray-100 text-gray-700"
          >
            <span class="mx-2 text-xl font-semibold">{{ path?.name }}</span>
          </RouterLink>
        </div>
      </nav>
    </div>
  </aside>
</template>
