<script setup>
import { onMounted, ref, watch } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute, useRouter } from 'vue-router'
import { useAuthUserStore } from '@/stores/authUserStore'
import {
  getPaymentDetailOfBookingForCustomerDashboard,
  confirmPaymentOfBookingForProviderDashboard,
  cancelPaymentOfBookingForProviderDashboard,
} from '@/services/customerService.js'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { formatDate } from '@/utils.js'
import { BookingStatus, PaymentMethods } from '@/constants'


const queryClient = useQueryClient()
const authUserStore = useAuthUserStore()
const router = useRouter()
const toast = useToast()
const route = useRoute()
const isEnabled = ref(false)
const custId = parseInt(authUserStore.customer.id)
const paymentId = route.params.paymentId

const paymentMethod = ref(PaymentMethods.CREDIT_CARD)

const {
  data: paymentData,
  isPending: isPaymentDataPending,
  refetch: refetchPaymentDetails,
  isError: isPaymentDataError,
  error: paymnetDataError,
  isStale,
  isFetched,
} = useQuery({
  queryKey: () => [],
  queryFn: () => getPaymentDetailOfBookingForCustomerDashboard(custId, paymentId),
  enabled: isEnabled.value,
  keepPreviousData: true,
})

const {
  isPending: isConfirmPending,
  isSuccess: isConfirmSuccess,
  mutate: confirmPaymentMutate,
  error: confirmError,
  isError: isConfirmError,
} = useMutation({
  mutationFn: () =>
    confirmPaymentOfBookingForProviderDashboard(custId, paymentId, { paymentMethod: paymentMethod.value }),
})

const {
  isPending: isCancelPending,
  isSuccess: isCancelSuccess,
  mutate: cancelPaymentMutate,
  error: cancelError,
  isError: isCancelError,
} = useMutation({
  mutationFn: () =>
    cancelPaymentOfBookingForProviderDashboard(custId, paymentId),
})

onMounted(async () => {
  console.log(isStale.value, isFetched.value)
  isEnabled.value = true
  refetchPaymentDetails()
})

watch([isPaymentDataError, paymnetDataError], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || 'Failed to fetch booking data')
  }
})

watch(paymentData, () => {
  console.log({ ...paymentData })
})


watch(confirmError, (errorVal) => {
  if (isConfirmError.value && errorVal) {
    toast.error(errorVal.message || 'Failed to confirm payment!!')
    router.push({ name: 'home' })
  }
})

watch(cancelError, (errorVal) => {
  if (isCancelError.value && errorVal) {
    toast.error(errorVal.message || 'Failed to continue service!!')
    router.push({ name: 'home' })
  }
})

watch(isConfirmSuccess, (isConfirmSuccessVal) => {
  if (isConfirmSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'customers' &&
          query.queryKey[2] === 'bookings'
        )
      },
    })
    toast.success('Payment Confirmed..')
    router.push({ name: 'customer-bookings', params: { custId } })
  }
})

watch(isCancelSuccess, (isCancelSuccessVal) => {
  if (isCancelSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'customers' &&
          query.queryKey[2] === 'bookings' &&
          query.queryKey[4] === BookingStatus.PENDING
        )
      },
    })
    toast.success('Payment and Booking cancellled...')
    router.push({ name: 'customer-bookings', params: { custId } })
  }
})

const handleConfirmPayment = () => {
  confirmPaymentMutate()
}

const handleCancelPayment = () => {
  cancelPaymentMutate()
}

watch(paymentMethod, () => {

  console.log(paymentMethod.value);
})

</script>

<template>
  <div class="w-full h-full min-h-screen bg-gray-100 flex flex-col items-center justify-center">
    <LoadingState v-if="isPaymentDataPending" />
    <ErrorState v-else-if="isPaymentDataError" />

    <div v-else class="w-[40%] bg-white shadow-lg rounded-lg overflow-hidden px-5 py-4">
      <div class="px-6 py-5">
        <h2 class="text-xl font-semibold text-gray-900">Payment Details</h2>
        <dl class="divide-y divide-gray-200">
          <div class="py-3 flex justify-between">
            <dt class="text-sm font-medium text-gray-500">Payer</dt>
            <dd class="text-lg font-medium text-green-500">
              {{ paymentData.payment.booking.customer.user.profile.first_name  }}
              {{ paymentData.payment.booking.customer.user.profile.last_name  }}
            </dd>
          </div>

          <div class="py-3 flex justify-between">
            <dt class="text-md font-medium text-gray-500">Invoice</dt>
            <dd class="text-md text-gray-900">
              # 123456
            </dd>
          </div>
          <div class="py-3 flex justify-between">
            <dt class="text-md font-medium text-gray-500">Booking Amount</dt>
            <dd class="text-md text-gray-900">{{ paymentData.payment.amount }} ₹</dd>
          </div>
          <div class="py-3 flex justify-between">
            <dt class="text-md font-medium text-gray-500">Platform Charge</dt>
            <dd class="text-md text-gray-900">{{ paymentData.payment.platform_fee }} ₹</dd>
          </div>
          <div class="py-3 flex justify-between">
            <dt class="text-md font-medium text-gray-500">Transaction Charge</dt>
            <dd class="text-md text-gray-900">{{ paymentData.payment.transaction_fee }} ₹</dd>
          </div>

          <div class="py-3 flex justify-between">
            <dt class="text-md font-medium text-gray-500">Total Amount</dt>
            <dd class="text-lg font-bold text-blue-600">{{ paymentData.payment.amount + paymentData.payment.platform_fee + paymentData.payment.transaction_fee }} ₹</dd>
          </div>

          <div class="py-3 flex justify-between">
            <dt class="text-md font-medium text-gray-500">Due Date</dt>
            <dd class="text-md font-semibold text-gray-900">
              {{ formatDate(paymentData.payment.booking.fullfillment_date) }}
            </dd>
          </div>
        </dl>
      </div>

      <div class="px-6">
        <label for="method" class="block mb-2 text-sm font-medium text-gray-500"
          >Payment Method
        </label>
        <select
          v-model="paymentMethod"
          class="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
        >

          <option :value="b" v-for="[a, b] in Object.entries(PaymentMethods)" :key="a">{{ a }}</option>

        </select>

        <div class="flex gap-5 justify-end mt-5">
          <button
            @click="handleConfirmPayment"
            :disabled="isConfirmPending || isCancelPending"
            class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-1 px-4 rounded-md transition duration-200"
          >
            Confirm
          </button>
          <button
            @click="handleCancelPayment"
            :disabled="isConfirmPending || isCancelPending"
            class="bg-red-500 hover:bg-red-600 text-white font-semibold py-1 px-4 rounded-md transition duration-200"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
