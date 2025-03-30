<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import {
  getAllCustomersForAdminDashboard,
  unblockCustomerForAdminDashboard,
  blockCustomerForAdminDashboard,
} from '@/services/adminService.js'

import PaginationBar from '@/components/PaginationBar.vue'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { formatDate } from '@/utils.js'

const queryClient = useQueryClient()
const toast = useToast()
const route = useRoute()

const isEnabled = ref(false)
const page = ref(route.query.page ? parseInt(route.query.page) : 1)

const {
  data: customerData,
  isPending: isCustomerDataPending,
  refetch: refetchCustomers,
  isError: isCustomerDataError,
  error: customerDataError,
} = useQuery({
  queryKey: () => ['admin', 'customers', page.value],
  queryFn: async () => await getAllCustomersForAdminDashboard(page.value),
  enabled: isEnabled.value,
  keepPreviousData: true,
})

const {
  data: blockedCustData,
  isPending: isBlockPending,
  isSuccess: isBlockSuccess,
  mutate: blockProvider,
  error: blockError,
  isError: isBlockError,
} = useMutation({
  mutationFn: ({ custId, custUsername }) =>
    blockCustomerForAdminDashboard({ custId, custUsername }),
})

const {
  data: unblockedCustData,
  isPending: isUnblockPending,
  isSuccess: isUnblockSuccess,
  mutate: unblockProvider,
  error: unblockError,
  isError: isUnblockError,
} = useMutation({
  mutationFn: ({ custId, custUsername }) =>
    unblockCustomerForAdminDashboard({ custId, custUsername }),
})

onMounted(() => {
  isEnabled.value = true
  refetchCustomers()
})

watch(customerDataError, (errorVal) => {
  if (isCustomerDataError.value && errorVal) {
    toast.error('Failed to fetch customers data!!')
  }
})

watch(blockError, (errorVal) => {
  if (isBlockError.value && errorVal) {
    toast.error(`Failed to block customer ${blockedCustData.value.custUsername}!!`)
  }
})

watch(unblockError, (errorVal) => {
  if (isUnblockError.value && errorVal) {
    toast.error(`Failed to unblock customer ${unblockedCustData.value.custUsername}!!`)
  }
})

watch(isBlockSuccess, (isBlockSuccessVal) => {
  if (isBlockSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'admin' &&
          query.queryKey[1] === 'customers'
        )
      },
    })
    toast.success(`Customer ${blockedCustData.value.custUsername} blocked..`)
    refetchCustomers()
  }
})

watch(isUnblockSuccess, (isUnblockSuccessVal) => {
  if (isUnblockSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'admin' &&
          query.queryKey[1] === 'customers'
        )
      },
    })
    toast.success(`Customer ${unblockedCustData.value.custUsername} unblocked..`)
    refetchCustomers()
  }
})

watch(
  () => route.query.page,
  (newPage) => {
    page.value = newPage ? parseInt(newPage) : 1
    refetchCustomers()
  },
)

const isActionButtonsDisabled = computed(() => isBlockPending.value || isUnblockPending.value)

const handleBlockCustomer = async (custId, custUsername) => {
  blockProvider({ custId, custUsername })
}

const handleUnblockCustomer = async (custId, custUsername) => {
  unblockProvider({ custId, custUsername })
}
</script>

<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
    <div
      class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0"
    >
      <div>
        <h2 class="text-lg font-semibold">All Customers</h2>
        <p class="mt-1 text-sm text-gray-700">This is a list of customers</p>
      </div>
    </div>
    <LoadingState v-if="isCustomerDataPending" />
    <ErrorState v-else-if="isCustomerDataError" />

    <div v-else class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
      <table class="min-w-full bg-white text-sm">
        <thead class="text-left bg-gray-50 uppercase">
          <tr class="text-center">
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Cust Id
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Name</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Location
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Total Bookings
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Status
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Joined
            </th>
            <th scope="col" class="px-4 py-2">Action</th>
          </tr>
        </thead>

        <tbody
          class="divide-y divide-gray-200"
          v-for="(cust, i) in customerData.customers"
          :key="i"
        >
          <tr class="odd:bg-white even:bg-gray-50 text-center">
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">{{ cust.id }}</td>
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              {{ cust.user.profile.first_name }}
            </td>
            <td class="whitespace-nowrap px-4 py-2">{{ cust.user.profile.location }}</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ cust.total_bookings }}</td>

            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              <span
                v-if="cust.is_blocked"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700 bg-red-100"
              >
                blocked
              </span>
              <span
                v-else
                class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700 bg-green-100"
              >
                active
              </span>
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{ formatDate(cust.created_at) }}
            </td>
            <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
              <button
                v-if="!cust.is_blocked"
                :disabled="isActionButtonsDisabled"
                @click="() => handleBlockCustomer(cust.id, cust.user.username)"
                :class="isActionButtonsDisabled ? 'bg-red-300 cursor-none' : 'bg-red-600 hover:bg-red-700'"
                class="inline-block rounded px-4 py-2 text-xs font-medium text-white"
              >
                Block
              </button>
              <button
                v-if="cust.is_blocked"
                :disabled="isActionButtonsDisabled"
                @click="() => handleUnblockCustomer(cust.id, cust.user.username)"
                :class="isActionButtonsDisabled ? 'bg-teal-300 cursor-none': 'bg-teal-600 hover:bg-teal-700'"
                class="inline-block rounded px-4 py-2 text-xs font-medium text-white"
              >
                Unblock
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <PaginationBar
      v-if="!isCustomerDataPending && !isCustomerDataError"
      :total="customerData?.no_customers"
      :pages="customerData?.no_of_pages"
      :currentPage="page"
      :perPage="customerData?.per_page"
      :path="{ name: route.name, query: { page } }"
    />
  </section>
</template>
