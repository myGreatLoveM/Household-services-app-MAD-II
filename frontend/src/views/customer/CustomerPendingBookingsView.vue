<script setup>
import { onMounted, ref, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import { useAuthUserStore } from '@/stores/authUserStore'
import { getAllBookingForCustomerDashboard } from '@/services/customerService.js'
import PaginationBar from '@/components/PaginationBar.vue'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { formatDate } from '@/utils.js'
import { BookingStatus } from '@/constants.js'


const authUserStore = useAuthUserStore()
const toast = useToast()
const route = useRoute()

const isEnabled = ref(false)
const page = ref(route.query.page ? parseInt(route.query.page) : 1)
const custId = parseInt(authUserStore.customer.id)

const {
  data: bookingData,
  isPending: isBookingDataPending,
  refetch: refetchBookings,
  isError: isBookingDataError,
  error: bookingDataError,
} = useQuery({
  queryKey: () => ['customers', custId, 'bookings', page.value, BookingStatus.PENDING],
  queryFn: () => getAllBookingForCustomerDashboard(custId, page.value, BookingStatus.PENDING),
  enabled: isEnabled.value,
  keepPreviousData: true,
})


onMounted(async () => {
  isEnabled.value = true
  refetchBookings()
})

watch([isBookingDataError, bookingDataError], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || 'Failed to fetch booking data')
  }
})

watch(
  () => route.query.page,
  (newPage) => {
    page.value = newPage ? parseInt(newPage) : 1
    refetchBookings()
  },
)

</script>

<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
    <div
      class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0"
    >
      <div>
        <h2 class="text-lg font-semibold">Pending Bookings</h2>
        <p class="mt-1 text-sm text-gray-700">
          This is a list of all pending, rejected, cancelled bookings.
        </p>
      </div>
    </div>

    <LoadingState v-if="isBookingDataPending" />
    <ErrorState v-else-if="isBookingDataError" />
    <div
      class="text-xl font-medium w-full text-center mt-10"
      v-else-if="bookingData?.bookings?.length === 0"
    >
      No bookings ...
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
              Category
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Provider
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
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              {{ booking.service.provider.category.name.toUpperCase() }}
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{
                booking.service.provider.user.profile.first_name +
                ' ' +
                booking.service.provider.user.profile.last_name
              }}
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
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700 bg-red-100"
              >
                rejected
              </span>
              <span
                v-else-if="booking.status === BookingStatus.CANCEL"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700 bg-red-100"
              >
                cancelled
              </span>
              <span
                v-else-if="booking.status === BookingStatus.CONFIRM"
                class="whitespace-nowrap rounded-full border border-purple-500 px-2.5 py-0.5 text-sm text-purple-700 bg-purple-100"
              >
                confirmed
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
              <RouterLink v-if="booking.payment" :to="{ name: 'booking-payment' , params: { custId, paymentId: booking.payment.id }}">
                <button
                  v-if="booking.status === BookingStatus.CONFIRM"
                  class="inline-block rounded bg-emerald-600 px-4 py-2 text-xs font-medium text-white hover:bg-emerald-700"
                >
                  Pay
                </button>
              </RouterLink>
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
