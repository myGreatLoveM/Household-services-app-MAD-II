<script setup>
import { onMounted, ref, watch } from 'vue'
import { useQuery, useMutation } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import { getAllBookingsForAdminDashboard, exportClosedBookingDataForAdmin } from '@/services/adminService.js'

import PaginationBar from '@/components/PaginationBar.vue'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { formatDate } from '@/utils.js'
import { PaymentStatus, BookingStatus } from '@/constants.js'



const toast = useToast()
const route = useRoute()

const isEnabled = ref(false)
const page = ref(route.query.page ? parseInt(route.query.page) : 1)

const { data, isPending, refetch, isError, error } = useQuery({
  queryKey: () => ['admin', 'bookings', page.value],
  queryFn: async () => await getAllBookingsForAdminDashboard(page.value),
  enabled: isEnabled.value,
  keepPreviousData: true,
})

const {
  isPending: isExportPending,
  isSuccess: isExportSuccess,
  mutate: exportMutate,
  error: exportError,
  isError: isExportError,
} = useMutation({
  mutationFn: () => exportClosedBookingDataForAdmin(),
  retry: 0
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
    toast.error(errorVal.message || 'Failed to fetch bookings data')
  }
})

watch(exportError, (errorVal) => {
  if (isExportError.value && errorVal) {
    toast.error(errorVal.message || 'Failed to export booking data !!')
  }
})

watch(isExportSuccess, (isExportSuccessVal) => {
  if (isExportSuccessVal) {
    toast.success('Export starting...')
  }
})


const handleExport = async () => {
  exportMutate()
}
</script>

<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
    <div
      class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0"
    >
      <div>
        <h2 class="text-lg font-semibold">All Bookings</h2>
        <p class="mt-1 text-sm text-gray-700">This is a list of all bookings</p>
      </div>

      <button
        @click="handleExport"
        @diabled="isExportPending"
        class="rounded-md bg-zinc-600 hover:bg-zinc-700 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
      >
        Closed Bookings Data CSV Export
      </button>
    </div>
    <LoadingState v-if="isPending" />
    <ErrorState v-else-if="isError" />

    <div v-else class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
      <table class="min-w-full divide-gray-200 bg-white text-sm">
        <thead class="text-center bg-gray-50 uppercase">
          <tr class="">
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Booking Id
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Service
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Category
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Provider
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Customer
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Service Price
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Booking Date
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
               Status
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Payment Status
            </th>
          </tr>
        </thead>

        <tbody class="divide-y divide-gray-200 text-center">
          <tr class="odd:bg-white even:bg-gray-50" v-for="(booking, i) in data.bookings" :key="i">
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">{{booking.id}}</td>
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">{{booking.service.name}}</td>
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">{{booking.service.provider.category.name}}</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ booking.service.provider.user.username }}</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ booking.customer.user.username }}</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ booking.service.price }} ₹</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ formatDate(booking.book_date) }}</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              <span
                v-if="booking.status === BookingStatus.PENDING"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
              >
                pending
              </span>
              <span
                v-if="booking.status === BookingStatus.REJECT"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
              >
                rejected
              </span>
              <span
                v-else-if="booking.status === BookingStatus.CANCEL"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
              >
                cancelled
              </span>
              <span
                v-else-if="booking.status === BookingStatus.CONFIRM"
                class="whitespace-nowrap rounded-full border border-purple-500 px-2.5 py-0.5 text-sm text-purple-700 bg-purple-100"
              >
                confirmed
              </span>
              <span
                v-else-if="booking.status === BookingStatus.ACTIVE"
                class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700 bg-green-100"
              >
                active
              </span>
              <span
                v-else-if="booking.status === BookingStatus.COMPLETE && !booking.is_closed"
                class="whitespace-nowrap rounded-full border border-pink-500 px-2.5 py-0.5 text-sm text-pink-700 bg-pink-100"
              >
                completed
              </span>
              <span
                v-else-if="booking.status === BookingStatus.COMPLETE && booking.is_closed"
                class="whitespace-nowrap rounded-full border border-zinc-500 px-2.5 py-0.5 text-sm text-zinc-700 bg-zinc-100"
              >
                closed
              </span>
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              <span
                v-if="booking.payment && booking.payment.status === PaymentStatus.PENDING"
                class="whitespace-nowrap rounded-full border border-yellow-500 px-2.5 py-0.5 text-sm text-yellow-700"
              >
                pending
              </span>
              <span
                v-else-if="booking.payment && booking.payment.status === PaymentStatus.CANCEL"
                class="whitespace-nowrap rounded-full border border-yellow-500 px-2.5 py-0.5 text-sm text-yellow-700"
              >
                cancelled
              </span>
              <span
                v-else-if="booking.payment && booking.payment.status === PaymentStatus.PAID"
                class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700"
              >
                paid
              </span>
              <span v-else>-</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <PaginationBar
      v-if="!isPending && !isError"
      :total="data?.no_of_bookings"
      :pages="data?.no_of_pages"
      :currentPage="page"
      :perPage="data?.per_page"
      :path="{ name: route.name, query: { page } }"
    />
  </section>
</template>
