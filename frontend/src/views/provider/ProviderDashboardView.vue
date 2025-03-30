<script setup>
import { onMounted, ref, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { getDashboardDataForProviderDashboard } from '@/services/providerService.js'


const toast = useToast()
const route = useRoute()

const isEnabled = ref(false)
const provId = route.params.provId

const { data, isPending, refetch, isError, error } = useQuery({
  queryKey: () => ['providers', provId, 'dashboard'],
  queryFn: () => getDashboardDataForProviderDashboard(provId),
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
    <LoadingState v-if="isPending" />
    <ErrorState v-else-if="isError" />

    <div v-else>
      <div class="bg-white rounded-lg mb-8">
        <div class="grid grid-cols-4 gap-4 mb-4">
          <div class="bg-gray-100 p-4 rounded-lg">
            <p class="text-lg font-bold text-gray-700">Total Active Services</p>
            <p class="text-2xl font-bold text-indigo-600">{{ data.total_active_services }}</p>
          </div>
          <div class="bg-gray-100 p-4 rounded-lg">
            <p class="text-lg font-bold text-gray-700">Avg Booking amount</p>
            <p class="text-2xl font-bold text-yellow-600">₹ {{ data.avg_booking_amount }}</p>
          </div>
          <div class="bg-gray-100 p-4 rounded-lg">
            <p class="text-lg font-bold text-gray-700">Total Pending Payments</p>
            <p class="text-2xl font-bold text-yellow-600">₹ {{ data.total_pending_earning }}</p>
          </div>
          <div class="bg-gray-100 p-4 rounded-lg">
            <p class="text-lg font-bold text-gray-700">Total Lifetime Earning</p>
            <p class="text-2xl font-bold text-yellow-600">₹ {{ data.total_lifetime_earning }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg mb-8">
        <div class="grid grid-cols-4 gap-4 mb-4">
          <div class="bg-gray-100 p-4 rounded-lg">
            <p class="text-lg font-bold text-gray-700">
              Avg Customer Rating :
              <span class="text-normal font-bold text-green-600">{{ data.avg_rating }}</span>
            </p>
            <p class="text-lg font-bold text-gray-700">
              No of reviews :
              <span class="text-normal font-bold text-green-600">{{ data.total_reviews }}</span>
            </p>
          </div>
          <div class="bg-gray-100 p-4 rounded-lg">
            <p class="text-lg font-bold text-gray-700">Total Bookings</p>
            <p class="text-2xl font-bold text-indigo-600">{{ data.total_bookings }}</p>
          </div>
          <div class="bg-gray-100 p-4 rounded-lg">
            <p class="text-lg font-bold text-gray-700">Active Bookings</p>
            <p class="text-2xl font-bold text-indigo-600">{{ data.active_bookings }}</p>
          </div>
          <div class="bg-gray-100 p-4 rounded-lg">
            <p class="text-lg font-bold text-gray-700">Closed Bookings</p>
            <p class="text-2xl font-bold text-green-600">{{ data.active_bookings }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
