<script setup>
import { onMounted, ref, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import { getAllPaymentsForAdminDashboard } from '@/services/adminService.js'

import PaginationBar from '@/components/PaginationBar.vue'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { formatDate } from '@/utils.js'
import {PaymentStatus} from '@/constants.js'

const toast = useToast()
const route = useRoute()

const isEnabled = ref(false)
const page = ref(route.query.page ? parseInt(route.query.page) : 1)

const { data, isPending, refetch, isError, error } = useQuery({
  queryKey: () => ['admin', 'payments', page.value],
  queryFn: async () => await getAllPaymentsForAdminDashboard(page.value),
  enabled: isEnabled.value,
  keepPreviousData: true,
})

onMounted(async () => {
  isEnabled.value = true
  refetch()
})

watch(
  () => route.query.page,
  (newPage) => {
    page.value = newPage ? parseInt(newPage) : 1
    refetch()
  },
)

watch([isError, error], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || 'Failed to fetch payments data')
  }
})
</script>

<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
    <div
      class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0"
    >
      <div>
        <h2 class="text-lg font-semibold">All Payments</h2>
        <p class="mt-1 text-sm text-gray-700">This is a list of payments for confirmed bookings</p>
      </div>
    </div>
    <LoadingState v-if="isPending" />
    <ErrorState v-else-if="isError" />

    <div v-else class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
      <table class="min-w-full bg-white text-sm">
        <thead class="text-left bg-gray-50 uppercase">
          <tr class="text-center">
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Payment Id
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Booking Id
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Customer
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              status
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Platform fee
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Transaction fee
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Booking Amount
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Payed on
            </th>
          </tr>
        </thead>

        <tbody class="divide-y divide-gray-200">
          <tr class="odd:bg-white even:bg-gray-50 text-center" v-for="(payment, i) in data.payments" :key="i">
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">{{payment.id}}</td>
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              {{payment.booking.id}}
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{payment.booking.customer.user.username}}
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              <span
                v-if="payment.status === PaymentStatus.PENDING"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
              >
                pending
              </span>
              <span
                v-else-if="payment.status === PaymentStatus.CANCEL"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
              >
                cancelled
              </span>
              <span
                v-else-if="payment.status === PaymentStatus.PAID"
                class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700"
              >
                paid
              </span>
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{ payment.status === PaymentStatus.PAID ? payment.platform_fee + ' ₹' : '-'}}
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{ payment.status === PaymentStatus.PAID ? payment.transaction_fee + ' ₹' : '-'}}
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{payment.amount}} ₹</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{ formatDate(payment.updated_at) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
     <PaginationBar
      v-if="!isPending && !isPending"
      :total="data?.no_of_payments"
      :pages="data?.no_of_pages"
      :currentPage="page"
      :perPage="data?.per_page"
      :path="{ name: route.name, query: { page } }"
    />
  </section>
</template>
