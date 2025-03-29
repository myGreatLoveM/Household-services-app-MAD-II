<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import PaginationBar from '@/components/PaginationBar.vue'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { formatDate } from '@/utils.js'
import {
  getAllBookingsForProviderDashboard,
  confirmBookingForProviderDashboard,
  rejectBookingForProviderDashboard,
} from '@/services/providerService'
import { useAuthUserStore } from '@/stores/authUserStore'
import { BookingStatus } from '@/constants'

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
  queryKey: () => ['providers', provId, 'bookings', page.value, BookingStatus.PENDING],
  queryFn: () => getAllBookingsForProviderDashboard(provId, page.value, BookingStatus.PENDING),
  enabled: isEnabled.value,
  keepPreviousData: true,
})

const {
  data: rejectBookingData,
  isPending: isRejectPending,
  isSuccess: isRejectSuccess,
  mutate: rejectBookingMutate,
  error: rejectError,
  isError: isRejectError,
} = useMutation({
  mutationFn: (bookingId) => rejectBookingForProviderDashboard(provId, bookingId),
})

const {
  data: confirmBookingData,
  isPending: isConfirmPending,
  isSuccess: isConfirmSuccess,
  mutate: confirmBookingMutate,
  error: confirmError,
  isError: isConfirmError,
} = useMutation({
  mutationFn: (bookingId) => confirmBookingForProviderDashboard(provId, bookingId),
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

watch(rejectError, (errorVal) => {
  if (isRejectError.value && errorVal) {
    toast.error(`Failed to reject booking ${confirmBookingData.value.bookingId}!!`)
  }
})

watch(confirmError, (errorVal) => {
  if (isConfirmError.value && errorVal) {
    toast.error(`Failed to confirm booking ${confirmBookingData.value.bookingId}!!`)
  }
})

watch(isRejectSuccess, (isRejectSuccessVal) => {
  if (isRejectSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'providers' &&
          query.queryKey[2] === 'bookings' &&
          query.queryKey[4] === BookingStatus.PENDING
        )
      },
    })
    toast.success(`Booking with id ${rejectBookingData.value.bookingId} rejected..`)
    refetchBookings()
  }
})

watch(isConfirmSuccess, (isConfirmSuccessVal) => {
  if (isConfirmSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'providers' &&
          query.queryKey[2] === 'bookings'
        )
      },
    })
    toast.success(`Booking with id ${confirmBookingData.value.bookingId} confirmed..`)
    refetchBookings()
  }
})

watch(
  () => route.query.page,
  (newPage) => {
    page.value = newPage ? parseInt(newPage) : 1
    refetchBookings()
  },
)

const isActionButtonsDisabled = computed(() => isRejectPending.value || isConfirmPending.value)

const handleRejectBooking = async (bookingId) => {
  rejectBookingMutate(bookingId)
}

const handleConfirmBooking = async (bookingId) => {
  confirmBookingMutate(bookingId)
}
</script>

<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
    <div
      class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0"
    >
      <div>
        <h2 class="text-lg font-semibold">New Bookings</h2>
        <p class="mt-1 text-sm text-gray-700">
          This is a list of all pending or rejected bookings.
        </p>
      </div>
    </div>

    <LoadingState v-if="isBookingDataPending" />
    <ErrorState v-else-if="isBookingDataError" />
    <div
      class="text-xl font-medium w-full text-center mt-10"
      v-else-if="bookingData?.bookings.length === 0"
    >
      No Pending or Rejected bookings
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
              Location
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Status
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
              {{ booking.customer.user.profile.location }}
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
               <span
                v-if="booking.status === BookingStatus.PENDING"
                class="whitespace-nowrap rounded-full border border-yellow-500 px-2.5 py-0.5 text-sm text-yellow-700"
              >
                pending
              </span>
              <span
                v-else-if="booking.status === BookingStatus.REJECT"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
              >
                rejected
              </span>
              <span
                v-else-if="booking.status === BookingStatus.CANCEL"
                class="whitespace-nowrap rounded-full border border-violet-500 px-2.5 py-0.5 text-sm text-violet-700"
              >
                cancelled
              </span>
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{ formatDate(booking.book_date) }}
            </td>
            <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
              <RouterLink :to="{ name: 'provider-single-booking', params: {bookingId: booking.id} }">
                <button
                  @disabled="isActionButtonsDisabled"
                  :class="isActionButtonsDisabled ? 'bg-indigo-400' : 'bg-indigo-600 hover:bg-indigo-700' "
                  class="inline-block rounded  px-4 py-2 text-xs font-medium text-white "
                >
                  View
                </button>
              </RouterLink>
              <button
                v-if="booking.status === BookingStatus.PENDING"
                @click="() => handleConfirmBooking(booking.id)"
                @disabled="isActionButtonsDisabled"
                :class="isActionButtonsDisabled ? 'bg-green-400' : 'bg-green-600 hover:bg-green-700' "
                class="inline-block rounded px-4 py-2 text-xs font-medium text-white"
              >
                Confirm
              </button>
              <button
                v-if="booking.status === BookingStatus.PENDING"
                @click="() => handleRejectBooking(booking.id)"
                @disabled="isActionButtonsDisabled"
                :class="isActionButtonsDisabled ? 'bg-red-400' : 'bg-red-600 hover:bg-red-700' "
                class="inline-block rounded  px-4 py-2 text-xs font-medium text-white"
              >
                Reject
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
