<script setup>
import { onMounted, ref, watch } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import { useAuthUserStore } from '@/stores/authUserStore'
import { getAllBookingForCustomerDashboard, completeBookingForProviderDashboard } from '@/services/customerService.js'
import PaginationBar from '@/components/PaginationBar.vue'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { formatDate } from '@/utils.js'
import { BookingStatus } from '@/constants.js'


const queryClient = useQueryClient()
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
  isStale,
  isFetched
} = useQuery({
  queryKey: () => ['customers', custId, 'bookings', page.value, BookingStatus.ACTIVE],
  queryFn: () => getAllBookingForCustomerDashboard(custId, page.value, BookingStatus.ACTIVE),
  enabled: isEnabled.value,
  keepPreviousData: true,
})

const {
  data: completeBookingData,
  isPending: isCompletePending,
  isSuccess: isCompleteSuccess,
  mutate: completeBookingMutate,
  error: completeError,
  isError: isCompleteError,
} = useMutation({
  mutationFn: (bookingId) =>
    completeBookingForProviderDashboard(custId, bookingId),
})


onMounted(async () => {
  console.log(isStale.value, isFetched.value);

  isEnabled.value = true
  refetchBookings()
})

watch([isBookingDataError, bookingDataError], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || 'Failed to fetch booking data')
  }
})


watch(completeError, (errorVal) => {
  if (isCompleteError.value && errorVal) {
    toast.error(`Failed to complete booking ${completeBookingData.value.bookingId}!!`)
  }
})


watch(isCompleteSuccess, (isCompleteSuccessVal) => {
  if (isCompleteSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'providers' &&
          query.queryKey[2] === 'services'
        )
      },
    })
    toast.success(`Booking with ID ${completeBookingData.value.bookingId} complete..`)
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

const handleCompleteBooking = async (bookingId) => {
  completeBookingMutate(bookingId)
}

</script>

<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
    <div
      class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0"
    >
      <div>
        <h2 class="text-lg font-semibold">All Bookings</h2>
        <p class="mt-1 text-sm text-gray-700">This is a list of all active or completed bookings.</p>
      </div>

      <div class="flex items-center gap-10">
        <RouterLink :to="{ name: 'customer-pending-bookings', params: { custId } }">
          <button
            class="rounded-md bg-zinc-600 hover:bg-zinc-700 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
          >
            Pending Bookings
          </button>
        </RouterLink>
      </div>
    </div>

    <LoadingState v-if="isBookingDataPending" />
    <ErrorState v-else-if="isBookingDataError" />
    <div
      class="text-xl font-medium w-full text-center mt-10"
      v-else-if="bookingData?.bookings?.length === 0"
    >
      No active or completed bookings..
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
                v-if="booking.status === BookingStatus.ACTIVE"
                class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700 bg-green-100"
              >
                active
              </span>
              <span
                v-if="booking.status === BookingStatus.COMPLETE"
                class="whitespace-nowrap rounded-full border border-pink-500 px-2.5 py-0.5 text-sm text-pink-700 bg-pink-100"
              >
                completed
              </span>
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{ formatDate(booking.book_date) }}
            </td>
            <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
              <button
                :disabled="isCompletePending"
                :class="isCompletePending ? 'bg-indigo-400' : 'bg-indigo-600 hover:bg-indigo-700'"
                class="inline-block rounded px-4 py-2 text-xs font-medium text-white"
              >
                View
              </button>
              <button
                v-if="booking.status === BookingStatus.ACTIVE"
                @click="() => handleCompleteBooking(booking.id)"
                :disabled="isCompletePending"
                :class="isCompletePending ? 'bg-pink-400' : 'bg-pink-600 hover:bg-pink-700'"
                class="inline-block rounded  px-4 py-2 text-xs font-medium text-white "
              >
                Complete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <PaginationBar
      v-show="!isCompletePending"
      v-if="!isBookingDataPending && !isBookingDataError"
      :total="bookingData?.no_of_bookings"
      :pages="bookingData?.no_of_pages"
      :currentPage="page"
      :perPage="bookingData?.per_page"
      :path="{ name: route.name, query: { page } }"
    />
  </section>
</template>
