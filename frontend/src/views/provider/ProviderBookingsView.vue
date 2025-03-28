<script setup>
import { onMounted, ref, watch } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import PaginationBar from '@/components/PaginationBar.vue'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { formatDate } from '@/utils.js'
import {
  getAllBookingsForProviderDashboard,
  closeBookingForProviderDashboard,
  exportClosedBookingData,
} from '@/services/providerService'
import { useAuthUserStore } from '@/stores/authUserStore'
import { BookingStatus, PaymentStatus } from '@/constants'

const queryClient = useQueryClient()
const authUserStore = useAuthUserStore()
const toast = useToast()
const route = useRoute()

const isEnabled = ref(false)
const page = ref(route.query.page ? parseInt(route.query.page) : 1)
const provId = parseInt(authUserStore.provider.id)

const {
  data: bookingData,
  isPending: isBookingDataPending,
  refetch: refetchBookings,
  isError: isBookingDataError,
  error: bookingDataError,
} = useQuery({
  queryKey: () => ['providers', provId, 'bookings', page.value, BookingStatus.ACTIVE],
  queryFn: () => getAllBookingsForProviderDashboard(provId, page.value, BookingStatus.ACTIVE),
  enabled: isEnabled.value,
  keepPreviousData: true,
})

const {
  data: closeBookingData,
  isPending: isClosePending,
  isSuccess: isCloseSuccess,
  mutate: closeBookingMutate,
  error: closeError,
  isError: isCloseError,
} = useMutation({
  mutationFn: (bookingId) => closeBookingForProviderDashboard(provId, bookingId),
})


const {
  isPending: isExportPending,
  isSuccess: isExportSuccess,
  mutate: exportMutate,
  error: exportError,
  isError: isExportError,
} = useMutation({
  mutationFn: () => exportClosedBookingData(provId),
  retry: 0
})


onMounted(async () => {
  isEnabled.value = true
  refetchBookings()
})

watch([isBookingDataError, bookingDataError], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || 'Failed to fetch booking data!!')
  }
})

watch(closeError, (errorVal) => {
  if (isCloseError.value && errorVal) {
    toast.error(`Failed to close booking ${closeBookingData.value.bookingId}!!`)
  }
})

watch(exportError, (errorVal) => {
  if (isExportError.value && errorVal) {
    toast.error(errorVal.message || 'Failed to export booking data !!')
  }
})

watch(isCloseSuccess, (isCloseSuccessVal) => {
  if (isCloseSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'providers' &&
          query.queryKey[2] === 'bookings' &&
          query.queryKey[4] === BookingStatus.ACTIVE
        )
      },
    })
    toast.success(`Booking with ID ${closeBookingData.value.bookingId} closed..`)
    refetchBookings()
  }
})


watch(isExportSuccess, (isExportSuccessVal) => {
  if (isExportSuccessVal) {
    toast.success('Export starting...')
  }
})

watch(
  () => route.query.page,
  (newPage) => {
    page.value = newPage ? parseInt(newPage) : 1
    refetchBookings()
  },
)

const handleExport = async () => {
  exportMutate()
}

const handleCloseBooking = async (bookingId) => {
  closeBookingMutate(bookingId)
}
</script>

<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
    <div
      class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0"
    >
      <div>
        <h2 class="text-lg font-semibold">All Bookings</h2>
        <p class="mt-1 text-sm text-gray-700">This is a list of all active bookings.</p>
      </div>

      <div class="flex items-center gap-10">
        <button
          @click="handleExport"
          @diabled="isExportPending"
          class="rounded-md bg-zinc-600 hover:bg-zinc-700 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
        >
          Export CSV Closed Bookings
        </button>
        <RouterLink :to="{ name: 'provider-pending-bookings', params: { provId } }">
          <button
            class="rounded-md bg-zinc-600 hover:bg-zinc-700 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
          >
            New Bookings
          </button>
        </RouterLink>
      </div>
    </div>

    <LoadingState v-if="isBookingDataPending" />
    <ErrorState v-else-if="isBookingDataError" />
    <div
      class="text-xl font-medium w-full text-center mt-10"
      v-else-if="bookingData?.bookings.length === 0"
    >
      No active bookings..
    </div>

    <div v-else class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
      <table class="min-w-full divide-gray-200 bg-white text-sm">
        <thead class="text-left bg-gray-50 uppercase">
          <tr class="text-center">
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Booking ID
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Service
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Customer
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Status
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Payment Status
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Booking Date
            </th>
            <th scope="col" class="px-4 py-2">Action</th>
          </tr>
        </thead>

        <tbody class="divide-y divide-gray-200">
          <tr
            class="odd:bg-white even:bg-gray-50 text-center"
            v-for="(booking, i) in bookingData.bookings"
            :key="i"
          >
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">{{ booking.id }}</td>
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              {{ booking.service.name.toUpperCase() }}
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{
                booking.customer.user.profile.first_name +
                ' ' +
                booking.customer.user.profile.last_name
              }}
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              <span
                v-if="booking.status === BookingStatus.CONFIRM"
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
                v-else-if="booking.is_closed"
                class="whitespace-nowrap rounded-full border border-zinc-500 px-2.5 py-0.5 text-sm text-zinc-700 bg-zinc-100"
              >
                closed
              </span>
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              <span
                v-if="booking.payment.status === PaymentStatus.PENDING"
                class="whitespace-nowrap rounded-full border border-yellow-500 px-2.5 py-0.5 text-sm text-yellow-700"
              >
                pending
              </span>
              <span
                v-else-if="booking.payment.status === PaymentStatus.PAID"
                class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700"
              >
                paid
              </span>
              <span
                v-else-if="booking.payment.status === PaymentStatus.CANCEL"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
              >
                cancelled
              </span>
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{ formatDate(booking.book_date) }}
            </td>
            <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
              <button
                class="inline-block rounded bg-indigo-600 px-4 py-2 text-xs font-medium text-white hover:bg-indigo-700"
              >
                View
              </button>
              <button
                v-if="booking.status === BookingStatus.COMPLETE && !booking.is_closed"
                @click="() => handleCloseBooking(booking.id)"
                :disabled="isClosePending"
                :class="isClosePending ? 'bg-zinc-400' : 'bg-zinc-600 hover:bg-zinc-700'"
                class="inline-block rounded px-4 py-2 text-xs font-medium text-white"
              >
                Close
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <PaginationBar
      v-if="!isBookingDataPending && !isBookingDataError"
      :total="bookingData?.no_of_bookings"
      :pages="bookingData?.no_of_pages"
      :currentPage="page"
      :perPage="bookingData?.per_page"
      :path="{ name: route.name, query: { page } }"
    />
  </section>
</template>
