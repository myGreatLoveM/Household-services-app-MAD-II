<script setup>
import { onMounted, ref, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { getDashboardDataForCustomerDashboard } from '@/services/customerService'

const toast = useToast()
const route = useRoute()

const isEnabled = ref(false)
const custId = route.params.custId

const { data, isPending, refetch, isError, error } = useQuery({
  queryKey: () => ['customers', custId, 'dashboard'],
  queryFn: () => getDashboardDataForCustomerDashboard(custId),
  enabled: isEnabled.value,
  keepPreviousData: true,
})

onMounted(async () => {
  isEnabled.value = true
  refetch()
})

watch([isError, error], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || 'Failed to fetch dashboard data!!')
  }
})
</script>

<template>
  <div class="container h-full mx-auto px-6 rounded-lg">
    <div class="bg-white rounded-lg mb-8">
      <LoadingState v-if="isPending" />
      <ErrorState v-else-if="isError" />

      <div v-else class="grid grid-cols-4 gap-4 mb-4">
        <div class="bg-gray-100 p-4 rounded-lg">
          <p class="text-lg font-bold text-gray-700">Total Bookings</p>
          <p class="text-2xl font-bold text-indigo-600">{{ data.total_bookings }}</p>
        </div>
        <div class="bg-gray-100 p-4 rounded-lg">
          <p class="text-lg font-bold text-gray-700">Active Bookings</p>
          <p class="text-2xl font-bold text-indigo-600">{{ data.active_bookings }}</p>
        </div>
        <div class="bg-gray-100 p-4 rounded-lg">
          <p class="text-lg font-bold text-gray-700">Completed Bookings</p>
          <p class="text-2xl font-bold text-green-600">{{ data.completed_bookings }}</p>
        </div>
        <div class="bg-gray-100 p-4 rounded-lg">
          <p class="text-lg font-bold text-gray-700">Lifetime Spent</p>
          <p class="text-2xl font-bold text-yellow-600">₹ {{ data.total_spent }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
