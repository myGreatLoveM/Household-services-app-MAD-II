<script setup>
import { reactive, watch, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { useRoute } from 'vue-router'
import ModalCloseButton from '@/components/ModalCloseButton.vue'
import InputField from '@/components/InputField.vue'
import { createReviewForCompletedBooking } from '@/services/customerService.js'

import { parseNumericFields, trimObjectStringValues } from '@/utils'

const props = defineProps({
  closeReviewModal: { type: Function },
})

const queryClient = useQueryClient()
const toast = useToast()
const route = useRoute()

const custId = route.params.custId
const bookingId = route.params.bookingId

const reviewFormFields = {
  rating: '',
  comment: '',
}

const reviewForm = reactive({ ...reviewFormFields })
const reviewFormError = reactive({ ...reviewFormFields })

const isSubmitButtonDisabled = computed(() => {
  return (
    Object.values(reviewFormError).some((err) => err !== '') || reviewForm.rating == ''
  )
})

watch(
  () => ({ ...reviewForm }),
  () => {
    if (!reviewForm.rating) {
      reviewFormError.rating = 'rating is required'
    } else if (!isNaN(reviewForm.rating) && parseInt(reviewForm.rating) > 6) {
      reviewFormError.rating = 'rating should not be above 5'
    } else {
      reviewFormError.rating = ''
    }
  },
  { deep: true },
)

const { isPending, isError, error, isSuccess, mutate } = useMutation({
  mutationFn: (reviewData) => createReviewForCompletedBooking(custId, bookingId, reviewData),
})

watch([isError, error], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || 'Failed to created review!!')
  }
})

watch(isSuccess, () => {
  queryClient.invalidateQueries({
    predicate: (query) => {
      return (
        Array.isArray(query.queryKey) &&
        query.queryKey[0] === 'customers' &&
        query.queryKey[1] === custId &&
        query.queryKey[2] === 'bookings' &&
        query.queryKey[3] === bookingId
      )
    },
  })
  toast.success('New review created successfully')
  emit('create-review')
  props.closeReviewModal()
})

function handleCreateReview() {
  if (isSubmitButtonDisabled.value) {
    return toast.error('Review Form is invalid!!!')
  }

  const reviewData = trimObjectStringValues(parseNumericFields({ ...reviewForm }))

  mutate(reviewData)
}

const emit = defineEmits(['create-review'])
</script>

<template>
  <div
    class="overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 flex justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full"
  >
    <div class="relative p-4 w-full max-w-md max-h-full">
      <div class="relative bg-emerald-700 rounded-lg shadow">
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
          <h3 class="text-lg font-semibold text-white">Review</h3>
          <ModalCloseButton @click="closeReviewModal" />
        </div>

        <div class="p-4 md:p-5">
          <div class="grid gap-4 mb-4 grid-cols-2">
            <div class="col-span-2">
              <InputField
                id="rating"
                label="Rating"
                labelInfo="(in 1-5)"
                type="number"
                placeholder="Enter rating"
                v-model="reviewForm.rating"
                :error="reviewFormError.rating"
                classForLabel="block mb-2 text-sm font-medium text-white"
                classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
              />
            </div>
            <div class="col-span-2">
              <InputField
                id="comment"
                label="Comment"
                type="text"
                placeholder="Write about booking experience"
                v-model="reviewForm.comment"
                :error="reviewFormError.comment"
                classForLabel="block mb-2 text-sm font-medium text-white"
                classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
              />
            </div>
          </div>
          <button
            @click="handleCreateReview"
            :disabled="isSubmitButtonDisabled || isPending"
            :class="
              isSubmitButtonDisabled || isPending
                ? 'bg-blue-500  cursor-none'
                : 'bg-blue-700 hover:bg-blue-800'
            "
            class="text-white inline-flex items-center font-medium rounded-lg text-sm px-5 py-2.5 text-center"
          >
            {{ isPending ? 'Creating...' : 'Create' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
