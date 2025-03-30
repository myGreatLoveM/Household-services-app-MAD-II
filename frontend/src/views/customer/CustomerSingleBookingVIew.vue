<script setup>
import { onMounted, ref, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { formatDate } from '@/utils.js'
import { getBookingForCustomerDashboard } from '@/services/customerService'
import { BookingStatus, PaymentStatus } from '@/constants'
import ReviewModal from '@/modals/ReviewModal.vue'
import RatingStar from '@/components/RatingStar.vue'

const toast = useToast()
const route = useRoute()
const isReviewModalOpen = ref(false)
const isEnabled = ref(false)
const custId = route.params.custId
const bookingId = route.params.bookingId

const {
  data: bookingData,
  isPending: isBookingDataPending,
  refetch: refetchBooking,
  isError: isBookingDataError,
  error: bookingDataError,
} = useQuery({
  queryKey: () => ['customers', custId, 'bookings', bookingId],
  queryFn: () => getBookingForCustomerDashboard(custId, bookingId),
  enabled: isEnabled.value,
  keepPreviousData: true,
})

onMounted(async () => {
  isEnabled.value = true
  refetchBooking()
})

watch([isBookingDataError, bookingDataError], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || 'Failed to fetch booking data!!')
  }
})

const openReviewModal = () => {
  isReviewModalOpen.value = true
  emit('review-modal-open')
}

const closeReviewModal = () => {
  isReviewModalOpen.value = false
  emit('review-modal-close')
}

const emit = defineEmits(['review-modal-open', 'review-modal-close'])
</script>

<template>
  <LoadingState v-if="isBookingDataPending" />
  <ErrorState v-else-if="isBookingDataError" />

  <div
    v-else
    :class="isReviewModalOpen && 'opacity-50'"
    class="bg-white shadow-lg rounded-lg p-8 mb-8 max-w-4xl mx-auto border border-gray-200"
  >
    <div class="flex items-center justify-between mb-6">
      <div class="space-y-1">
        <h2 class="text-3xl font-semibold text-gray-800">
          Booking ID #{{ bookingData.booking.id }}
        </h2>
        <h5 class="text-sm text-gray-600">{{ formatDate(bookingData.booking.book_date) }}</h5>
      </div>

      <span class="text-sm text-gray-500"
        >Status:
        <span class="font-semibold text-green-500">{{ bookingData.booking.status }}</span></span
      >
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-8 mb-8">
      <div class="bg-gray-50 p-6 rounded-lg shadow-sm space-y-2">
        <h3 class="text-lg font-medium text-gray-700 mb-4">Provider Information</h3>
        <p class="text-gray-600">
          Name:
          <span class="font-semibold">{{
            bookingData.booking.service.provider.user.profile.first_name +
            ' ' +
            bookingData.booking.service.provider.user.profile.last_name
          }}</span>
        </p>
        <p class="text-gray-600">
          Location:
          <span class="font-semibold">{{
            bookingData.booking.service.provider.user.profile.location
          }}</span>
        </p>
        <p class="text-gray-600">
          Email:
          <span class="font-semibold">{{ bookingData.booking.service.provider.user.email }}</span>
        </p>
        <p class="text-gray-600">
          Contact:
          <span class="font-semibold"
            >+91 {{ bookingData.booking.service.provider.user.profile.contact }}</span
          >
        </p>
      </div>

      <div class="bg-gray-50 p-6 rounded-lg shadow-sm space-y-2">
        <h3 class="text-lg font-medium text-gray-700 mb-4">Service Details</h3>
        <p class="text-gray-600">
          Service Title: <span class="font-semibold">{{ bookingData.booking.service.name }}</span>
        </p>
        <p class="text-gray-600">
          Category:
          <span class="font-semibold">{{
            bookingData.booking.service.provider.category.name
          }}</span>
        </p>
        <p class="text-gray-600">
          Price:
          <span class="font-semibold text-blue-500"
            >{{ bookingData.booking.service.price }} ₹/hr</span
          >
        </p>
        <p class="text-gray-600">
          Time Required:
          <span class="font-semibold">{{ bookingData.booking.service.time_required_hr }} hrs</span>
        </p>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-8 mb-8">
      <!-- Booking Info -->
      <div class="bg-gray-50 p-6 rounded-lg shadow-sm space-y-3">
        <div class="space-y-2">
          <h3 class="text-lg font-medium text-gray-700 mb-4">Booking Information</h3>
          <p class="text-gray-600">
            Booking Date:
            <span class="font-semibold">{{ formatDate(bookingData.booking.book_date) }}</span>
          </p>
          <p class="text-gray-600">
            Fullfillemnt Date:
            <span class="font-semibold">{{
              formatDate(bookingData.booking.fullfillment_date)
            }}</span>
          </p>
        </div>
        <div class="space-y-2" v-if="bookingData.booking.confirm_date">
          <p class="text-gray-600">
            Confirmed on:
            <span class="font-semibold">{{ formatDate(bookingData.booking.confirm_date) }}</span>
          </p>
          <p class="text-gray-600" v-if="bookingData.booking.complete_date">
            Completed on:
            <span class="font-semibold">{{ formatDate(bookingData.booking.complete_date) }}</span>
          </p>
          <p class="text-gray-600" v-if="bookingData.booking.closed_date">
            Closed on:
            <span class="font-semibold">{{ formatDate(bookingData.booking.closed_date) }}</span>
          </p>
        </div>
      </div>

      <div
        class="bg-gray-50 p-6 rounded-lg shadow-sm space-y-2"
        v-if="
          bookingData.booking.payment && bookingData.booking.payment.status === PaymentStatus.PAID
        "
      >
        <h3 class="text-lg font-medium text-gray-700 mb-4">Payment Information</h3>
        <p class="text-gray-600">
          Payment Status:
          <span class="font-semibold text-green-500">{{ bookingData.booking.payment.status }}</span>
        </p>
        <p class="text-gray-600">
          Booking amount :
          <span class="font-semibold">{{ bookingData.booking.payment.amount }} ₹</span>
        </p>
        <p class="text-gray-600">
          Commission :
          <span class="font-semibold">{{ bookingData.booking.payment.commission_fee }} ₹</span>
        </p>
        <p class="text-gray-600">
          Final amount:
          <span class="font-semibold text-blue-400"
            >{{
              bookingData.booking.payment.amount - bookingData.booking.payment.commission_fee
            }}
            ₹</span
          >
        </p>
        <p class="text-gray-600">
          Payment Date:
          <span class="font-semibold">{{
            formatDate(bookingData.booking.payment.updated_at)
          }}</span>
        </p>
      </div>
    </div>

    <div v-if="bookingData.booking.review" class="mt-4">
      <h4 class="text-md font-semibold text-gray-700 mb-2">Review</h4>
      <div class="space-y-4">
        <div class="bg-gray-100 p-4 rounded-lg">

          <div class="flex justify-between items-center">
            <p class="text-sm text-gray-00">{{ formatDate(bookingData.booking.review.created_at) }}</p>
            <div class="flex items-center">
              <RatingStar v-for="i in bookingData.booking.review.rating" :key="i" />
            </div>
          </div>

          <p class="overflow-wrap text-sm text-gray-600 mt-2">{{ bookingData.booking.review.comment }}</p>
        </div>
      </div>
    </div>

    <button
      v-if="bookingData.booking.status == BookingStatus.COMPLETE && !bookingData.booking.review"
      @click="openReviewModal"
      class="rounded-md bg-black px-5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
    >
      Review
    </button>
  </div>
  <ReviewModal
    v-if="isReviewModalOpen"
    :closeReviewModal="closeReviewModal"
    @create-review="refetchBooking"
  />
</template>
