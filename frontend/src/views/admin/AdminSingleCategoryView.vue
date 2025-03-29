<script setup>
import { onMounted, ref, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import { getCategoryForAdminDashboard } from '@/services/adminService.js'

import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import CategoryModal from '@/modals/CategoryModal.vue'
import { formatDate } from '@/utils.js'

const toast = useToast()
const route = useRoute()

const isEnabled = ref(false)
const isCategoryModelOpen = ref(false)
const catId = route.params.catId

const { data, isPending, refetch, isError, error } = useQuery({
  queryKey: () => ['admin', 'categories', catId],
  queryFn: async () => await getCategoryForAdminDashboard(catId),
  enabled: isEnabled.value,
  keepPreviousData: true,
})

onMounted(async () => {
  isEnabled.value = true
  refetch()
})

watch([isError, error], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || 'Failed to fetch data')
  }
})

const openCategoryModal = () => {
  isCategoryModelOpen.value = true
  emit('categoryModalOpen')
}

const closeCategoryModal = () => {
  isCategoryModelOpen.value = false
  emit('categoryModalClose')
}

const refetchCategory = () => {
  refetch()
}

const emit = defineEmits(['categoryModalOpen', 'categoryModalClose'])
</script>

<template>
  <LoadingState v-if="isPending" />
  <ErrorState v-else-if="isError" />

  <section v-else class="mx-auto w-full max-w-7xl px-4">
    <div :class="isCategoryModelOpen && 'opacity-50'" class="max-w-full bg-white border border-gray-200 rounded-lg shadow-lg p-6">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">{{ data.category.name }}</h2>
          <p class="text-sm">Created At: {{ formatDate(data.category.created_at) }}</p>
        </div>

        <div class="flex items-center gap-5">
          <p class="text-lg font-semibold text-gray-900">
            Base Price: {{ data.category.base_price }} ₹/hr
          </p>
          <button
            @click="openCategoryModal"
            :class="
              isPending ? 'bg-black/50 hover:bg-black/50 cursor-none' : 'bg-black hover:bg-black/80'
            "
            class="rounded-md px-3 py-2 text-sm font-semibold text-white shadow-sm"
          >
            Edit
          </button>
        </div>
      </div>

      <p class="text-gray-600 text-base mt-5">
        {{ data.category.long_description }}
      </p>

      <hr class="my-4 border-gray-300" />

      <div class="grid grid-cols-4 gap-4">
        <div class="bg-blue-100 p-4 rounded-lg text-center">
          <h5 class="text-xl font-bold text-blue-700">{{ data.category.active_providers }}</h5>
          <p class="text-sm text-blue-600">Service Providers</p>
        </div>
        <div class="bg-purple-100 p-4 rounded-lg text-center">
          <h5 class="text-xl font-bold text-purple-700">{{ data.category.active_services }}</h5>
          <p class="text-sm text-purple-600">Services Listed</p>
        </div>
        <div class="bg-yellow-100 p-4 rounded-lg text-center">
          <h5 class="text-xl font-bold text-yellow-700">{{ data.category.total_bookings }}</h5>
          <p class="text-sm text-yellow-600">Total Bookings</p>
        </div>
        <div class="bg-green-100 p-4 rounded-lg text-center">
          <h5 class="text-xl font-bold text-green-700">{{ data.category.total_revenue }} ₹</h5>
          <p class="text-sm text-green-600">Total Revenue</p>
        </div>
      </div>

      <!-- Other Category Info -->
      <div class="mt-3 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <div class="bg-gray-50 p-4 rounded-lg space-y-1 text-gray-500">
            <p>
              <span class="font-medium">Commission Rate:</span>
              {{ data.category.commission_rate }} %
            </p>
            <p><span class="font-medium">Booking Rate:</span> {{ data.category.booking_rate }} %</p>
            <p>
              <span class="font-medium">Transaction Rate:</span>
              {{ data.category.transaction_rate }} %
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
  <CategoryModal v-if="isCategoryModelOpen" 
    mode="UPDATE"
    :categoryData="data.category" 
    :closeCategoryModal="closeCategoryModal" 
    @update-category="refetchCategory"
  />
</template>
